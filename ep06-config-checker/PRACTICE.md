# EP 06 practice: settings and CLAUDE.md

Two parts. **Hands-on exercises** you run against `check-config.ts` and the
fixture repo, then **practice questions** in the exam's scenario style. Answers
are folded under each item, so try it first.

Every question here is original, written for this series, and is not drawn from
any real exam.

**Cost:** every exercise here is **FREE**. Nothing calls the Anthropic API.

---

## Part 1: hands-on

### 1. Fix the cold open

Move the deny rule from `fixtures/priya-repo/.claude/settings.local.json` into
`fixtures/priya-repo/.claude/settings.json`, under `permissions.deny`. Run
`npm run check` again.

<details><summary>What this shows</summary>

The first FLAG line is gone. The rule now lives in the committed file, so every
clone gets it. The local file can still hold a deny too; that's harmless. The
problem was only ever a rule that lived **nowhere else**.

</details>

### 2. Pin the model

In the same team file, replace `"sonnet"` with a full model name from the
current models page. Run the check.

<details><summary>What this shows</summary>

The second FLAG is gone. A nickname points at newer models over time; a full
model name doesn't move until you change the line. That line change is now a
reviewed commit, not something that happened to you.

</details>

### 3. Grow the rulebook

Append two hundred lines to `fixtures/priya-repo/CLAUDE.md` (any text). Run the
check.

<details><summary>What this shows</summary>

`CLAUDE.md` flips to FLAG. The limit in the file is the docs' size guidance at
the time of writing, not a hard limit in Claude Code. The point is the one from
the episode: a long rulebook gets skimmed, and the one rule that mattered gets
lost. Move folder-specific guidance into `.claude/rules/` with a `paths` glob.

</details>

### 4. Lose the edition

Delete the `edition: 4` line from `prompts/support.md`. Run the check.

<details><summary>What this shows</summary>

The prompt check flags. Without an edition, a wrong answer next month can't be
traced to the words that actually ran.

</details>

### 5. Stop a merge

Run `npm run check; echo $?` (or `npm run check; echo %ERRORLEVEL%` on Windows
`cmd`). With anything flagged, the exit code is 1. A CI step that runs this
check stops the merge.

---

## Part 2: practice questions

### Q1

Your team commits `.claude/settings.json` with `"model": "sonnet"`. One
developer's `.claude/settings.local.json` sets a different model. Which model
does Claude Code use for that developer, in that repo?

- A. The team's, because committed settings win
- B. The developer's local setting, because local sits above project
- C. Whichever was set most recently
- D. The user settings in their home folder

<details><summary>Answer</summary>

**B.** Local project settings sit above shared project settings in the
precedence order (managed, then command line flags, then local, then project,
then user). A is the trap: committed feels authoritative, but it isn't higher.

</details>

### Q2

Your project settings allow `Bash(npm test)`. A developer adds a deny rule for
`Bash(npm test)` in their **user** settings. What happens in that repo?

- A. The project allow wins, because project is above user
- B. The deny wins, because a deny from any level blocks the action
- C. Claude asks every time
- D. It depends on the permission mode

<details><summary>Answer</summary>

**B.** Rules are evaluated deny first, then ask, then allow, across every
settings level. A is the trap: the precedence order decides between two values
for the same key, but deny rules merge and still win.

</details>

### Q3

A team wants Claude Code to follow a strict SQL style only in `src/db/`. Where
should that guidance go?

- A. At the top of `CLAUDE.md`, in capitals
- B. A rules file in `.claude/rules/` with a `paths` glob for `src/db/**`
- C. A deny rule in project settings
- D. Each developer's local settings

<details><summary>Answer</summary>

**B.** A path-scoped rules file loads only when Claude works with matching
files, so it doesn't dilute the rulebook everywhere else. C blocks actions; it
doesn't teach style.

</details>

### Q4

A support bot's answers changed tone overnight. Nobody deployed. The config
names the model by alias. What is the most likely cause, and the fix?

- A. The prompt drifted. Shorten it
- B. The alias now points at a newer model. Pin the full model name and switch on purpose
- C. The cache expired. Warm it
- D. The user settings changed. Add a deny rule

<details><summary>Answer</summary>

**B.** An alias follows the recommended model over time. Pinning the full name
makes a model change a deliberate, reviewed, testable commit.

</details>
