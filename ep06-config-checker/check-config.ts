// check-config.ts - CCDV-F EP 06 companion.
//
// Reads a repo's Claude Code settings the way the layers stack, and flags
// what will not travel to the next machine:
//   1. a deny rule that lives only in the local file (git leaves it out)
//   2. a model set by alias ("nickname") instead of a full model name
//   3. a CLAUDE.md that has grown past the docs' size guidance
//   4. a system prompt with no edition (version) number
//
// It never calls the Anthropic API. No key, no spend.
// Usage: npm run check -- [repo] [home]
// Exit code 1 when anything is flagged, so a CI step can stop a merge.
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

type Settings = {
  model?: string;
  permissions?: { allow?: string[]; deny?: string[] };
};

// The three files a repo can see. Managed settings (head office) live on
// the machine, set by an administrator, above all three: never in a repo.
const USER = ".claude/settings.json"; // under your home folder
const TEAM = ".claude/settings.json"; // in the repo, committed
const NOTE = ".claude/settings.local.json"; // in the repo, git-ignored

// Claude Code's model aliases, from its model configuration docs. An alias
// points at newer models over time. Check the current list in the docs.
const ALIASES = ["default", "best", "sonnet", "opus", "haiku", "opusplan"];
const isAlias = (m?: string) =>
  !!m && ALIASES.includes(m.replace(/\[1m\]$/, ""));

// The docs' size target for one CLAUDE.md file. Check the current docs.
const MAX_LINES = 200;

const read = (p: string): Settings =>
  existsSync(p) ? JSON.parse(readFileSync(p, "utf8")) : {};
const text = (p: string) =>
  existsSync(p) ? readFileSync(p, "utf8") : "";
const countLines = (s: string) =>
  s.trimEnd().split("\n").length;
const editionOf = (s: string) =>
  s.match(/^edition: (\d+)$/m)?.[1] ?? "";

const repo = process.argv[2] ?? "fixtures/priya-repo";
const home = process.argv[3] ?? "fixtures/home";

let flags = 0;
const flag = (msg: string) => {
  flags += 1;
  console.log(`FLAG ${msg}`);
};
const check = (ok: boolean, msg: string) =>
  ok ? console.log(`PASS ${msg}`) : flag(msg);

// Lowest first. Higher layers win.
const user = read(join(home, USER));
const team = read(join(repo, TEAM));
const note = read(join(repo, NOTE));
// Scalar keys like "model": the higher layer wins, key by key.
const merged = { ...user, ...team,
  ...note };
const model = merged.model;

// Deny rules merge from every layer, and a deny beats any allow. But a
// deny that lives only in the note never reaches the next machine.
const denies = (s: Settings) =>
  s.permissions?.deny ?? [];
for (const rule of denies(note)) {
  if (!denies(team).includes(rule))
    flag(`deny ${rule}: local only`);
}

const rulebook = text(join(repo, "CLAUDE.md"));
const ed = editionOf(text(join(repo, "prompts/support.md")));

// The model moves if it's a nickname. The rulebook gets followed if it's
// short. The prompt can be traced if it carries an edition.
if (isAlias(model))
  flag(`model: alias "${model}"`);
const lines = countLines(rulebook);
check(lines <= MAX_LINES,
  `CLAUDE.md: ${lines} lines`);
check(!!ed, `prompt: edition ${ed}`);

process.exitCode = flags > 0 ? 1 : 0;
