# Support desk app

Team rulebook. Loaded by Claude Code at the start of every session.
Keep it short: if a rule only matters in one folder, it goes in
`.claude/rules/` with a `paths` glob instead.

## Commands

- Install: `npm install`
- Test: `npm test`
- Lint: `npm run lint`
- Run locally: `npm run dev`

## Conventions

- TypeScript, strict mode. No `any`.
- Functions and files use camelCase. Types use PascalCase.
- One exported function per file in `src/tools/`.
- Every tool description says what it does, what comes back, and when not
  to use it.

## Don't touch

- `src/billing/` without a person reviewing the change.
- `migrations/` that have already shipped. Add a new one instead.

## Prompts

- System prompts live in `prompts/`, one file each, with an `edition:` line.
- A prompt change is a new edition, reviewed like code, and run against the
  test set before it ships.

## Secrets

- Never read or print `.env`. The hard block is a deny rule in
  `.claude/settings.json`, not this line.
