"""EP 04: exercise classify.py's safety checks with NO API key and NO spend.

Move four says: a schema is not a success. Check how the response ended,
then parse defensively. This script proves those checks work by swapping the
real API call for fake responses, one per way a response can go wrong.

Run:  python check_offline.py

Every line should end in PASS. Nothing here calls the API or bills anything.
"""

from __future__ import annotations

import os
from types import SimpleNamespace

# classify.py builds an Anthropic client at import time. A placeholder key
# lets it import; no request is ever sent, because create() is replaced below.
os.environ.setdefault("ANTHROPIC_API_KEY", "offline-placeholder")

import classify  # noqa: E402


def fake(stop_reason: str, text: str | None):
    """A response shaped like the real one: stop_reason plus content blocks."""
    blocks = [] if text is None else [SimpleNamespace(type="text", text=text)]
    return SimpleNamespace(stop_reason=stop_reason, content=blocks)


CASES = [
    # (what we are simulating, fake response, expected label, expected flag)
    ("normal answer",           fake("end_turn", '{"label": "BILLING"}'),   "BILLING",   None),
    ("lower-case enum value",   fake("end_turn", '{"label": "technical"}'), "TECHNICAL", None),
    ("cut off by max_tokens",   fake("max_tokens", '{"lab'),               None, "max_tokens"),
    ("refusal",                 fake("refusal", "I can't help with that."), None, "refusal"),
    ("not JSON at all",         fake("end_turn", "BILLING"),               None, "unparseable"),
    ("JSON, wrong key",         fake("end_turn", '{"category": "BILLING"}'), None, "unparseable"),
    ("label outside the list",  fake("end_turn", '{"label": "REFUND"}'),    None, "unknown label"),
    ("no text block returned",  fake("end_turn", None),                    None, "unparseable"),
]


def main() -> int:
    failures = 0
    for name, response, want_label, want_flag in CASES:
        classify.client.messages.create = lambda r=response, **_kw: r
        got = classify.classify("I was charged twice for the same month.")
        ok = got["label"] == want_label and got["flagged"] == want_flag
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name:<24} -> {classify.show(got)}")
    print()
    print("All checks passed." if not failures else f"{failures} check(s) failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
