# CCDV-F EP 09 companion code

**Eval, testing and debugging.** The failure checker from the episode: a small
TypeScript script that reads recorded traces and, for each run that failed,
prints the step that broke, whether it is your code or the model, and whether to retry or fail
fast. Runnable code for [EP 09 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `checker.ts` | The checker built in the episode | **No** |
| `traces.json` | Five recorded runs of a courier support bot: a rate limit, a bad tool request, a confident wrong answer, a pass, and a refusal | No |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | None of the exercises need a key |

Nothing in this folder needs an Anthropic API key. The traces are recorded, so
the script runs the same way every time.

## Setup

You need Node.js 20 or newer.

```
npm install
npm run try
```

What it should print:

```
c1 call   code  RETRY, back off
c2 lookup code  FAIL FAST, fix input
c3 check  model FIX PROMPT, RE-EVAL
c4 PASS
c5 call   model FAIL FAST, refusal
```

Point it at your own traces with `npx tsx checker.ts my-traces.json`.

## The four moves, in this folder

| Move | Where it is |
|---|---|
| **Evals** | Not built here, because an eval needs your feature. `c3` is what an eval catches that no status code will: a well-formed answer that is wrong. The fix is the prompt, checked by re-running the eval |
| **Test levels** | `c2` is an integration failure: the tool wrapper and the order API each work alone, and the handover between them sends the wrong type |
| **Traces** | `traces.json`. Each run is a list of steps. `firstFail` finds the first step that broke, and `owner` says whether it is your code (`code`) or the model (`model`) |
| **Recovery** | `RETRY` holds the statuses time can fix: rate limit, overloaded, and server errors. `next` checks a refusal first, because a refusal arrives as a normal success, not an error |

## Course terms

The episode uses Ravi's courier service as its picture. The Skilljar course uses
these words, and so does the exam:

| In the episode | The real term |
|---|---|
| Twenty test parcels, scored before launch | An eval (a graded set of cases) |
| Each scanner, one delivery, the van-to-branch handover, shop to doorstep | Unit, functional, integration and end-to-end tests |
| The tracking scans | A trace |
| The label versus the driver's judgment | The integration layer versus the model's output |
| Customer not home, try tomorrow | A retriable error |
| No such address | A terminal error |
| The customer refuses the parcel | A refusal (`stop_reason: "refusal"`) |

## Check the docs

Status codes, retry behaviour and stop reasons can change. Check the current
pages before you rely on them:

- API errors (status codes, `retry-after`, SDK retries): https://platform.claude.com/docs/en/api/errors
- Stop reasons, including `refusal`: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- Returning tool errors with `is_error`: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls

Independent study material. Not affiliated with or endorsed by Anthropic.
