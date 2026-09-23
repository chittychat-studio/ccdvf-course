# CCDV-F EP 04 companion code

**Prompt and context engineering.** The support-ticket classifier from the
episode, onboarded properly. Runnable code for
[EP 04 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `classify.py` | The classifier built in the episode | Yes, three very small calls per default run |
| `check_offline.py` | Feeds `classify.py` fake responses to prove its safety checks work | **No.** No key, no spend |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | Some exercises do, each one says so |

## Setup

```
pip install -r requirements.txt
cp .env.example .env        # put your key in it
```

Get a key from [the Claude Console](https://console.anthropic.com/).
You need `anthropic` 1.0 or newer: older SDKs don't accept `output_config`
and fail with a `TypeError` before sending anything.

No key yet? Start with `python check_offline.py`. It needs neither a key
nor credits.

## `classify.py`

```
python classify.py
python classify.py "Login page shows a blank screen on Safari."
```

The default run sends three tickets. The third sets `max_tokens` to 1 on
purpose, so the answer runs out of room and is flagged instead of guessed.
What it should print:

```
BILLING
TECHNICAL
FLAGGED (max_tokens)
```

The third line comes from the code, not the model: a response cut off by
`max_tokens` never reaches the parser. The first two are the model's call,
held to the three allowed labels by the schema.

| Move | Where it is in the file |
|---|---|
| **The brief** | `SYSTEM`: role and rules. The ticket goes in the message, inside `<ticket>` tags |
| **The shape** | Three examples in `<example>` tags, each different, plus the exact labels allowed |
| **The check** | `output_config` with a JSON schema, then `stop_reason`, then a defensive parse |

Two details that go beyond what fits on screen:

- **The schema locks which labels are allowed, not their capitalisation.** The
  structured outputs docs say to compare enum values case-insensitively, so the
  parser upper-cases the label before checking it.
- **Model names change.** Set `CLAUDE_MODEL` in `.env` to any current model
  that supports structured outputs, rather than editing the file.

## `check_offline.py`

```
python check_offline.py
```

Replaces the API call with eight fake responses: a normal answer, a lower-case
label, a `max_tokens` cut-off, a refusal, plain text instead of JSON, the wrong
key, a label outside the list, and an empty reply. Every line should say
`PASS`. Then delete the `stop_reason` check in `classify.py` and run it again
to see what that check was protecting.

## Move three, the desk (no code)

Everything Claude sees sits in one context window. It has edges, and it doesn't
tidy itself. Four ways to keep it clear:

| Strategy | What it does | What you lose |
|---|---|---|
| **Rewind (pruning)** | Jump back to an earlier message and carry on from there | Everything after that point, useful parts included |
| **Compact** | Summarise the thread. Say what to keep: decisions, errors and fixes, files touched | Anything the summary leaves out |
| **Clear** | Start a fresh session for an unrelated task | All of it. Keep what matters in a file Claude reads every session, like `CLAUDE.md` |
| **Hand off to a subagent** | A separate context does the messy digging and returns a short answer | Visibility into how it got there |

In testing, inputs are small and the window never fills. Real tool outputs are
much bigger. Plan the budget for real inputs.

## What the exam cares about

- Rules that never change go in the system prompt. The task for this call goes in the message.
- Pasted text is data. Tags help Claude treat it that way. They aren't a lock.
- A prompt that fails needs the one missing piece, not more words.
- A schema isn't a success. Read `stop_reason` before you parse.
- Confident output isn't proof. Check the facts that matter.

## Sources

Current at the time of writing. Check them before you build on any of this.

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)

Independent study material. Not affiliated with or endorsed by Anthropic. Every
practice question here is original and is not drawn from any real exam.
