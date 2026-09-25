# CCDV-F EP 06 companion code

**Settings and CLAUDE.md.** The config checker from the episode: it reads a
repo's Claude Code settings the way the layers stack, and flags what won't
travel to the next machine. Runnable code for
[EP 06 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `check-config.ts` | The checker built in the episode | **No** |
| `fixtures/priya-repo/` | Priya's repo from the cold open: team settings, her local settings file, a `CLAUDE.md`, a versioned prompt | No |
| `fixtures/home/` | A stand-in for your home folder's user settings | No |
| `setup-fixtures.mjs` | Runs automatically before `npm run check`. The fixtures ship as `dot-claude/` and `dot-env` (many tools skip dot-names), and this copies them to `.claude/` and `.env`. It never overwrites an existing file | No |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | None of the exercises need a key |

Nothing in this folder needs an Anthropic API key. The `.env` in the fixture
is a fake, there so the deny rule has something to protect. The PRACTICE.md
exercises edit the copies in `.claude/`, which exist after your first
`npm run check`.

## Setup

You need Node 20 or newer.

```
npm install
npm run check
```

What it should print (the exit code is 1, because two things are flagged):

```
FLAG deny Read(./.env): local only
FLAG model: alias "sonnet"
PASS CLAUDE.md: 36 lines
PASS prompt: edition 4
```

Point it at your own repo with `npm run check -- <path-to-repo> <path-to-home>`.
`npm run typecheck` runs the TypeScript compiler with no output files.

## The four moves, in the file

| Move | Where it is in `check-config.ts` |
|---|---|
| **The layers** | `user`, `team`, `note` are read lowest first and spread into `merged`, so the higher layer wins key by key. Managed settings (head office) sit above all three but live on the machine, never in a repo |
| **The rulebook** | `countLines(rulebook)` against `MAX_LINES`. `CLAUDE.md` is context Claude reads, not a lock, so short beats long |
| **Pin the model** | `isAlias(model)` flags a nickname such as `sonnet`. Pin the full model name so every machine runs the same model |
| **Version the prompt** | `editionOf(...)` reads the `edition:` line from `prompts/support.md`. Log it with every request |

The four lines of output above are the ones shown on screen in the episode.

## Course terms

The episode uses an office rulebook binder as its picture. The Skilljar course
uses these words, and so does the exam:

| In the episode | The real term |
|---|---|
| Head office tab | Managed settings (`managed-settings.json`, set by an administrator) |
| Team tab | Project settings (`.claude/settings.json`, committed) |
| Sticky note | Local project settings (`.claude/settings.local.json`, kept out of git) |
| Habits | User settings (`~/.claude/settings.json`) |
| Rulebook | `CLAUDE.md` |
| Nickname | Model alias |
| Full name | Full model ID |
| Edition | Prompt version |

## Check the docs

Settings precedence, the alias list, and the size guidance for `CLAUDE.md` all
come from the Claude Code documentation on the day this was written. They
change. Check the current pages before you rely on them:

- Settings files and precedence: https://code.claude.com/docs/en/settings
- Permissions (allow, ask, deny): https://code.claude.com/docs/en/permissions
- Memory and `CLAUDE.md`: https://code.claude.com/docs/en/memory
- Model configuration and aliases: https://code.claude.com/docs/en/model-config
- Model IDs and versions (API): https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions

Independent study material. Not affiliated with or endorsed by Anthropic.
