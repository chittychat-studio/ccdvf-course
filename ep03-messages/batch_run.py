"""EP 03, move four: the Message Batches API.

Submit thousands of requests in one call, get a batch id, poll, download.
Cheaper per token than the synchronous API. The cost is latency: a batch can
take up to 24 hours, though most finish far sooner. Right for offline work.
Wrong for anything with a person waiting on it.

Limits and pricing change. Check before you design around them:
https://platform.claude.com/docs/en/build-with-claude/batch-processing

Run:  python batch_run.py submit records.jsonl
      python batch_run.py poll   msgbatch_xxx
      python batch_run.py fetch  msgbatch_xxx --out results.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from anthropic import Anthropic
from anthropic.types.messages.batch_create_params import Request
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-5"

PROMPT = (
    "Classify this support message into exactly one of: BILLING, BUG, "
    "FEATURE_REQUEST, OTHER. Reply with the label alone and nothing else.\n\n"
)


def build_requests(path: Path) -> list[Request]:
    """One line of input -> one request with a custom_id you can join back on.

    custom_id is how you match a result to its input. Results do NOT come back
    in submission order. Joining by position is a real bug waiting to happen.
    """
    requests = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        line = line.strip()
        if not line:
            continue
        requests.append(
            Request(
                custom_id=f"record-{i:06d}",
                params=MessageCreateParamsNonStreaming(
                    model=MODEL,
                    max_tokens=16,
                    messages=[{"role": "user", "content": PROMPT + line}],
                ),
            )
        )
    return requests


def submit(path: Path) -> str:
    client = Anthropic()
    requests = build_requests(path)
    print(f"submitting {len(requests)} requests")
    batch = client.messages.batches.create(requests=requests)
    print("batch id:", batch.id)
    print("processing_status:", batch.processing_status)
    return batch.id


def poll(batch_id: str, every: int = 60) -> None:
    """processing_status is one of in_progress, canceling, ended."""
    client = Anthropic()
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        print(
            f"{batch.processing_status:<12} "
            f"processing={counts.processing} succeeded={counts.succeeded} "
            f"errored={counts.errored} canceled={counts.canceled} expired={counts.expired}"
        )
        if batch.processing_status == "ended":
            return
        time.sleep(every)


def fetch(batch_id: str, out: Path) -> None:
    """Every result carries a type: succeeded, errored, canceled, expired.
    Only succeeded is billed. Handle all four; do not assume success."""
    client = Anthropic()
    tally = {"succeeded": 0, "errored": 0, "canceled": 0, "expired": 0}
    with out.open("w", encoding="utf-8") as fh:
        for result in client.messages.batches.results(batch_id):
            kind = result.result.type
            tally[kind] = tally.get(kind, 0) + 1
            row = {"custom_id": result.custom_id, "type": kind}
            if kind == "succeeded":
                row["label"] = result.result.message.content[0].text.strip()
            else:
                row["error"] = str(getattr(result.result, "error", ""))
            fh.write(json.dumps(row) + "\n")
    print("wrote", out, tally)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["submit", "poll", "fetch"])
    ap.add_argument("target")
    ap.add_argument("--out", type=Path, default=Path("results.jsonl"))
    ap.add_argument("--every", type=int, default=60)
    args = ap.parse_args()

    if args.action == "submit":
        submit(Path(args.target))
    elif args.action == "poll":
        poll(args.target, args.every)
    else:
        fetch(args.target, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
