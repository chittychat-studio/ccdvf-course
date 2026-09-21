"""EP 03, move one and two: assemble a streamed message, and never act early.

This is the handler built live in the episode. It does three things the
episode says a handler must do:

  1. Build the final message from the event series yourself.
  2. Never parse or run a tool call before its content_block_stop.
  3. On an interrupted stream, throw the partial turn away. Never save it.

Run:  python stream_handler.py
      python stream_handler.py --simulate-drop     (proves rule 3)
"""

from __future__ import annotations

import argparse
import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")

TOOLS = [
    {
        "name": "get_weather",
        "description": (
            "Get the current weather for a city. Use this whenever the user "
            "asks what the weather is like somewhere."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. Bengaluru"},
                "unit": {"type": "string", "enum": ["c", "f"], "default": "c"},
            },
            "required": ["city"],
        },
    }
]


class StreamAssembler:
    """Turns the event series into one finished message.

    `self.complete` is the whole point. It flips True only on message_stop.
    Anything else means what we have is provisional and must not be saved.
    """

    def __init__(self) -> None:
        self.blocks: list[dict] = []
        self._partial_json: dict[int, list[str]] = {}
        self.stop_reason: str | None = None
        self.usage: dict = {}
        self.complete = False

    # -- one method per event type, so the mapping is obvious ---------------

    def message_start(self, event) -> None:
        # A new message is beginning. Make an empty list to collect blocks in.
        self.blocks = []
        self._partial_json = {}
        self.complete = False

    def content_block_start(self, event) -> None:
        # A block is opening. Make a slot for it at its index.
        block = event.content_block
        while len(self.blocks) <= event.index:
            self.blocks.append(None)
        if block.type == "text":
            self.blocks[event.index] = {"type": "text", "text": "", "done": False}
        elif block.type == "tool_use":
            # Opens with name and id, but NO input yet. That is the trap.
            self.blocks[event.index] = {
                "type": "tool_use",
                "id": block.id,
                "name": block.name,
                "input": None,
                "done": False,
            }
            self._partial_json[event.index] = []
        elif block.type == "thinking":
            self.blocks[event.index] = {"type": "thinking", "thinking": "", "done": False}

    def content_block_delta(self, event) -> None:
        # A piece of that block arrived. Append it. Do not interpret it.
        slot = self.blocks[event.index]
        delta = event.delta
        if delta.type == "text_delta":
            slot["text"] += delta.text
        elif delta.type == "input_json_delta":
            # Partial JSON string. Not valid JSON yet. Collect, do not parse.
            self._partial_json[event.index].append(delta.partial_json)
        elif delta.type == "thinking_delta":
            slot["thinking"] += delta.thinking

    def content_block_stop(self, event) -> None:
        # THE moment a tool call's input becomes parseable. Not before.
        slot = self.blocks[event.index]
        slot["done"] = True
        if slot["type"] == "tool_use":
            raw = "".join(self._partial_json.get(event.index, []))
            slot["input"] = json.loads(raw) if raw else {}

    def message_delta(self, event) -> None:
        # Top-level news: why it stopped, and the final token counts.
        if getattr(event.delta, "stop_reason", None):
            self.stop_reason = event.delta.stop_reason
        if getattr(event, "usage", None):
            self.usage = event.usage.model_dump()

    def message_stop(self, event) -> None:
        self.complete = True

    # -- what callers are allowed to ask for --------------------------------

    def ready_tool_calls(self) -> list[dict]:
        """Only blocks that actually closed. A half-built call is invisible here."""
        if not self.complete:
            raise RuntimeError(
                "refusing to hand out tool calls from an incomplete stream. "
                "message_stop never arrived."
            )
        return [b for b in self.blocks if b and b["type"] == "tool_use" and b["done"]]

    def as_assistant_turn(self) -> dict:
        """The turn you are allowed to append to history. Complete or nothing."""
        if not self.complete:
            raise RuntimeError(
                "refusing to build an assistant turn from an interrupted stream. "
                "Discard this turn and retry the request."
            )
        content = []
        for b in self.blocks:
            if b is None or not b["done"]:
                continue
            if b["type"] == "text":
                content.append({"type": "text", "text": b["text"]})
            elif b["type"] == "tool_use":
                content.append(
                    {"type": "tool_use", "id": b["id"], "name": b["name"], "input": b["input"]}
                )
        return {"role": "assistant", "content": content}


HANDLERS = {
    "message_start": "message_start",
    "content_block_start": "content_block_start",
    "content_block_delta": "content_block_delta",
    "content_block_stop": "content_block_stop",
    "message_delta": "message_delta",
    "message_stop": "message_stop",
}


def run(messages: list[dict], simulate_drop_after: int | None = None) -> StreamAssembler:
    client = Anthropic()
    asm = StreamAssembler()
    seen = 0
    with client.messages.stream(
        model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
    ) as stream:
        for event in stream:
            # ping and error events exist too. ping is a keep-alive and
            # recovers nothing; there is no handler for it on purpose.
            name = HANDLERS.get(event.type)
            if name:
                getattr(asm, name)(event)
                seen += 1
            if simulate_drop_after is not None and seen >= simulate_drop_after:
                print(f"\n[simulated network drop after {seen} events]")
                break
    return asm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--simulate-drop",
        action="store_true",
        help="cut the stream mid tool call, to prove the discard path",
    )
    ap.add_argument("--prompt", default="What is the weather in Bengaluru right now?")
    args = ap.parse_args()

    history = [{"role": "user", "content": args.prompt}]
    asm = run(history, simulate_drop_after=6 if args.simulate_drop else None)

    if not asm.complete:
        # The whole lesson, in four lines.
        print("stream interrupted before message_stop")
        print("stop_reason so far:", asm.stop_reason)
        print("discarding the partial assistant turn. history is untouched.")
        print("history length still:", len(history))
        try:
            asm.as_assistant_turn()
        except RuntimeError as exc:
            print("guard held:", exc)
        return 1

    print("stop_reason:", asm.stop_reason)
    for block in asm.blocks:
        if block and block["type"] == "text":
            print("text:", block["text"].strip())
    for call in asm.ready_tool_calls():
        print("tool call ready:", call["name"], call["input"])
    history.append(asm.as_assistant_turn())
    print("history length now:", len(history))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
