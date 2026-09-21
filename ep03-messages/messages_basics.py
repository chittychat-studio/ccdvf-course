"""EP 03, move one: the Messages API itself.

Three things a request needs: `model`, `max_tokens`, `messages`.

Two things people get wrong, both demonstrated below:

  1. The system prompt is NOT a message. It is its own top-level `system`
     parameter, sitting beside `messages`.
  2. The API is stateless. It remembers nothing between calls. You resend
     the entire conversation every single turn. That is also why one
     corrupted turn in your history keeps breaking every request after it.

Docs: https://platform.claude.com/docs/en/api/messages

Run:  python messages_basics.py
      python messages_basics.py --show-growth
"""

from __future__ import annotations

import argparse

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-5"

# Its own parameter. Not messages[0]. This is the single most common
# mistake when porting from a chat-completions-shaped API.
SYSTEM = (
    "You are a terse assistant for a support team. "
    "Answer in one sentence. Never speculate."
)

# What each stop_reason means. Read it; do not assume the model finished.
STOP_REASONS = {
    "end_turn": "finished naturally",
    "max_tokens": "you cut it off with max_tokens",
    "stop_sequence": "hit one of your stop sequences",
    "tool_use": "it wants to call a tool",
    "pause_turn": "a long-running turn paused; continue it",
    "refusal": "the model declined",
    "model_context_window_exceeded": "generation hit the context window",
}


class Conversation:
    """Holds the history the client is responsible for, because the API is not.

    Every `send` posts the WHOLE list again. Nothing is stored server side.
    """

    def __init__(self) -> None:
        self.client = Anthropic()
        self.messages: list[dict] = []

    def send(self, user_text: str) -> str:
        # roles alternate: user, assistant, user, assistant, ...
        self.messages.append({"role": "user", "content": user_text})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=512,
            system=SYSTEM,          # <- beside messages, never inside it
            messages=self.messages,  # <- the entire history, every time
        )

        reason = response.stop_reason
        print(f"  stop_reason: {reason} ({STOP_REASONS.get(reason, 'unknown')})")
        if reason == "max_tokens":
            print("  NOTE: this answer is truncated. Raise max_tokens or ask for less.")

        # content is a LIST of blocks, not a string. Text is one block type
        # among several (image, document, tool_use, tool_result, thinking).
        text = "".join(b.text for b in response.content if b.type == "text")

        # Append the assistant turn so the next call carries it back.
        self.messages.append({"role": "assistant", "content": response.content})

        print(f"  history: {len(self.messages)} messages, "
              f"{response.usage.input_tokens} input tokens billed this turn")
        return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show-growth", action="store_true",
                    help="three turns, so you can watch input tokens climb")
    args = ap.parse_args()

    convo = Conversation()
    turns = ["A customer says their export button does nothing on Safari. Triage it."]
    if args.show_growth:
        turns += [
            "What is the single most likely cause?",
            "Give me one line to put in the bug ticket.",
        ]

    for i, turn in enumerate(turns, 1):
        print(f"\nturn {i}: {turn}")
        print(" ", convo.send(turn))

    if args.show_growth:
        print("\nInput tokens rose every turn even though you typed less.")
        print("That is statelessness: you paid to resend the whole conversation.")
        print("Managing that growth is what EP 04's context work is about.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
