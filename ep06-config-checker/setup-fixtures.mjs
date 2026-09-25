// setup-fixtures.mjs - runs automatically before `npm run check` (npm's
// "precheck" hook). Git hosting and some sync tools skip or block folders and
// files whose names start with a dot, so the fixtures ship as `dot-claude/`
// and `dot-env`, and this script copies them to the real names Claude Code
// uses: `.claude/` and `.env`. It never overwrites a file that already exists,
// so your own edits to the fixtures (PRACTICE.md exercises) survive re-runs.
import { cpSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import { join } from "node:path";

const pairs = [
  ["fixtures/priya-repo/dot-claude", "fixtures/priya-repo/.claude"],
  ["fixtures/home/dot-claude", "fixtures/home/.claude"],
];
for (const [from, to] of pairs) {
  mkdirSync(to, { recursive: true });
  for (const f of readdirSync(from)) {
    if (!existsSync(join(to, f))) cpSync(join(from, f), join(to, f));
  }
}
if (!existsSync("fixtures/priya-repo/.env")) cpSync("fixtures/priya-repo/dot-env", "fixtures/priya-repo/.env");
