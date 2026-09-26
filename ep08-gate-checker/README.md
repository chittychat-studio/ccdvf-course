# CCDV-F EP 08 companion code

**Requirements, the build life cycle, and the engineering basics.** The gate
checker from the episode: a small Python script that reads a requirements
record and a release file, and prints what blocks the next gate. Runnable
code for [EP 08 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `gate_check.py` | The checker built in the episode | **No** |
| `fixtures/ravi-plan/` | Ravi's first plan from the episode: a vague requirement, the wrong region, no eval yet | No |
| `fixtures/ravi-fixed/` | The same plan after the three fixes | No |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | None of the exercises need a key |

Nothing in this folder needs an Anthropic API key, and nothing needs installing.
Standard library only.

## Setup

You need Python 3.10 or newer.

```
python gate_check.py
```

What it should print (the exit code is 1, because three things are flagged):

```
FLAG R1: vague "faster"
PASS infra: all four
FLAG residency: us-east not india
PASS model: pinned
FLAG eval: not passed
```

Then run the fixed plan, which exits 0:

```
python gate_check.py fixtures/ravi-fixed
```

## The four moves, in this folder

| Move | Where it is |
|---|---|
| **Requirements** | `requirements.json`. `functional` holds checkable statements of what the system must do. `infrastructure` answers latency, scale, residency and identity. `VAGUE` in `gate_check.py` catches wishes like "faster" |
| **The life cycle and its gates** | Requirements, design, build, test, deploy, operate, iterate. The checker runs two gates: the design gate (the platform meets the residency rule) and the release gate (the model you tested is the one you ship, and the eval passed) |
| **Where it runs** | `release.json` `platform`. The customer's cloud usually decides, and residency and identity come from the platform, not your code |
| **The seams** | Not built here. Every join between parts is a trust boundary: fetched content is data, not instructions, and each part gets only the access its job needs |

## Course terms

The episode uses Ravi opening a new branch office as its picture. The Skilljar
course uses these words, and so does the exam:

| In the episode | The real term |
|---|---|
| What the branch has to do | Functional requirements |
| Commute time, headcount, the city, staff badges | Latency, scale, residency, identity (infrastructure requirements) |
| The fire inspection | A gate between life cycle phases |
| The city where the company holds its licence | The customer's cloud, which usually decides the deployment platform |
| A parcel at the front desk | Untrusted content crossing a trust boundary |
| A badge that opens only your rooms | Least privilege, per component |

## Check the docs

Model IDs, platform names and regional coverage change. The model ID in the
fixtures is only an example. Check the current pages before you rely on them:

- Model IDs and versioning: https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions
- Models overview: https://platform.claude.com/docs/en/about-claude/models/overview

Independent study material. Not affiliated with or endorsed by Anthropic.
