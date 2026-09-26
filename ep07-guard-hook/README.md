# CCDV-F EP 07 companion code

**Claude Code: permission modes, hooks and helpers (subagents, skills and plugins).** The guard hook from the
episode: a `PreToolUse` hook, in TypeScript, that reads one tool call and
blocks it if it deletes a folder or touches the secrets file. Runnable code
for [EP 07 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `guard.ts` | The guard hook built in the episode | **No** |
| `try-guard.ts` | Feeds sample tool calls into `guard.ts` the way Claude Code does (JSON on stdin) and prints what it decided. You don't need Claude Code installed | No |
| `calls.json` | The four sample calls from the episode | No |
| `settings.example.json` | The keycard (least-privilege allow and deny rules) and the hook wiring, ready to copy into a repo's `.claude/settings.json` | No |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | None of the exercises need a key |

Nothing in this folder needs an Anthropic API key.

## Setup

You need Node 20 or newer.

```
npm install
npm run try
```

What it should print:

```
BLOCK rm -rf fixtures
  Blocked: no folder deletes
BLOCK .env
  Blocked: secrets stay shut
ALLOW npm test
ALLOW src/app.ts
```

`npm run typecheck` runs the TypeScript compiler with no output files.

## Wire it into a real repo

1. Copy `guard.ts` into your repo's root (or change the path in the command).
2. Merge `settings.example.json` into your repo's `.claude/settings.json`.
3. Start Claude Code in that repo and ask it to delete a folder. The hook
   blocks the call and Claude sees the reason.

Commit `.claude/settings.json` so every clone gets the guard (EP 06: the team
tab travels, the sticky note stays home).

## The four moves, in this folder

| Move | Where it is |
|---|---|
| **The modes** | Not a file: pick one with Shift+Tab or `--permission-mode`. `default` asks before edits and commands, `acceptEdits` lets edits through, `plan` only reads and plans, `auto` has a second model check each action, `dontAsk` refuses anything not pre-approved, `bypassPermissions` skips every check (sealed containers only) |
| **The keycard** | `permissions.allow` / `permissions.deny` in `settings.example.json`. Least privilege: allow what the job needs, deny the rest. A deny wins over any allow, in every mode |
| **The hook** | `guard.ts`. Exit code 2 blocks the call and stderr goes back to Claude as the reason. Exit code 0 lets the call carry on to the normal permission check |
| **The helpers** | Not built here. Subagents live in `.claude/agents/`, skills in `.claude/skills/<name>/SKILL.md`, and a plugin bundles skills, agents, hooks and MCP servers into one install |

## Course terms

The episode uses Ravi's office as its picture. The Skilljar course uses these
words, and so does the exam:

| In the episode | The real term |
|---|---|
| Sign-off level | Permission mode |
| "Don't ask me" | `bypassPermissions` |
| Keycard | Allow and deny rules (permissions in settings.json) |
| Helpers | Subagents, skills (and custom commands) and plugins |
| Guard on the door | Hook (`PreToolUse`) |
| Rulebook | `CLAUDE.md` |
| Runner | Subagent |
| How-to card | Skill (`SKILL.md`) |
| Starter kit | Plugin |

## Check the docs

Mode names, hook events and the plugin format come from the Claude Code
documentation on the day this was written. They change (the default mode is
labelled Manual in newer versions, for example, and auto mode depends on your
plan). Check the current pages before you rely on them:

- Permission modes: https://code.claude.com/docs/en/permission-modes
- Permissions (allow, ask, deny): https://code.claude.com/docs/en/permissions
- Hooks: https://code.claude.com/docs/en/hooks
- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Plugins: https://code.claude.com/docs/en/plugins

Independent study material. Not affiliated with or endorsed by Anthropic.
