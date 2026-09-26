// guard.ts - CCDV-F EP 07 companion. A PreToolUse hook.
//
// Claude Code runs this BEFORE a tool call. It pipes the call in as JSON on
// stdin. Exit code 2 blocks the call, and whatever we print to stderr goes
// back to Claude as the reason. Exit code 0 lets the call carry on to the
// normal permission check.
//
// The difference from a line in CLAUDE.md: a CLAUDE.md line is advice Claude
// reads and usually follows. This runs on every matching tool call, whatever
// the model decides. The guard at the door, not the sign on the wall.
//
// It never calls the Anthropic API. No key, no spend.
import { readFileSync } from "node:fs";

type Input = { command?: string;
  file_path?: string };
type Call = { tool_name: string;
  tool_input: Input };

// The guard's list. Short on purpose.
const RULES: [RegExp, string][] = [
  [/\brm -\w*r/, "no folder deletes"],
  [/\.env\b/, "secrets stay shut"],
];

const call: Call =
  JSON.parse(readFileSync(0, "utf8"));
const target =
  call.tool_input.command ??
  call.tool_input.file_path ?? "";

for (const [re, why] of RULES) {
  if (re.test(target)) {
    console.error(`Blocked: ${why}`);
    process.exit(2);
  }
}
process.exit(0);
