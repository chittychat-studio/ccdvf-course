# EP 07 practice: permission modes, hooks and helpers (subagents, skills, plugins)

Two parts. **Hands-on exercises** you run against `guard.ts`, then **practice
questions** in the exam's scenario style. Answers are folded under each item,
so try it first.

Every question here is original, written for this series, and is not drawn from
any real exam.

**Cost:** every exercise here is **FREE**. Nothing calls the Anthropic API.

---

## Part 1: hands-on

### 1. Add a rule

Add a third rule to `RULES` in `guard.ts` that blocks `git push --force`.
Add a matching call to `calls.json` and run `npm run try`.

<details><summary>What this shows</summary>

The new call prints BLOCK with your reason. A guard rule is one pattern and one
reason. Keep the list short: every rule runs on every matching call.

</details>

### 2. Watch exit code 1 fail open

Change `process.exit(2)` to `process.exit(1)` and run the tester again.

<details><summary>What this shows</summary>

Everything prints ALLOW. Only exit code 2 blocks. Any other non-zero code is a
non-blocking error and the call carries on. A guard that exits with the wrong
code is a guard asleep at the door.

</details>

### 3. Move the rule into the keycard (the allow and deny rules)

Delete the `.env` rule from `guard.ts`. Check that `settings.example.json`
still denies `Read(./.env)`.

<details><summary>What this shows</summary>

A deny rule in settings blocks the read in every mode, without any script.
Use the keycard for "never touch this path". Use a hook when the decision
needs logic a pattern can't express.

</details>

### 4. A PostToolUse side job

Sketch a second hook in `settings.example.json` under `PostToolUse` that runs
your formatter after `Edit`.

<details><summary>What this shows</summary>

PostToolUse runs after the call has happened, so it can't block. It's the
right place for side jobs: format, test, log.

</details>

### 5. Close the gap in the matcher

Look at `"matcher": "Bash|Read|Edit"` in `settings.example.json`. Which tool
that changes files does it miss? Add it.

<details><summary>What this shows</summary>

`Write` creates a brand-new file and isn't covered, so a new file could be
written without the guard ever seeing it. A matcher is part of the guard: a
tool it doesn't name walks straight past the door.

</details>

---

## Part 2: practice questions

### Q1

You're exploring an unfamiliar repo before a risky refactor. You want Claude to
read and propose, and to change nothing until you approve. Which mode?

- A. acceptEdits
- B. plan
- C. dontAsk
- D. bypassPermissions

<details><summary>Answer</summary>

**B.** Plan mode reads and writes a plan; edits wait for your approval. A lets
edits through. C refuses anything not pre-approved, which is for scripts and
CI, not exploration. D removes every check.

</details>

### Q2

Project settings allow `Bash(rm *)`. Managed settings deny `Bash(rm -rf *)`.
A developer runs Claude in bypassPermissions mode. Claude tries `rm -rf build`.
What happens?

- A. It runs, because bypass skips every check
- B. It runs, because the project allow matches
- C. It's blocked, because a deny wins in every mode
- D. Claude asks first

<details><summary>Answer</summary>

**C.** Deny rules block in every mode, including bypassPermissions, and a deny
beats an allow wherever it's written.

</details>

### Q3

You delegate a code search to the built-in Explore subagent. Its answer ignores
a rule from your CLAUDE.md. Why, and what's the fix?

- A. The rule is too long. Shorten CLAUDE.md
- B. Explore skips CLAUDE.md. Use the general-purpose subagent or a custom one
- C. Subagents never read files. Paste the rule in the prompt
- D. The hook blocked it. Remove the hook

<details><summary>Answer</summary>

**B.** Explore and Plan skip CLAUDE.md to stay fast. For work where your
project rules must apply, use the general-purpose subagent or a custom subagent.

</details>

### Q4

Your team's deploy workflow must only ever run when someone types the command
on purpose, never because Claude decided it was relevant. How do you package it?

- A. A line in CLAUDE.md
- B. A skill with `disable-model-invocation: true`
- C. A PostToolUse hook
- D. A subagent with no tools

<details><summary>Answer</summary>

**B.** A skill with `disable-model-invocation: true` runs only when you call it
by name, with a slash. Claude can't load it on its own.

</details>
