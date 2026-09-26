// try-guard.ts - feeds sample tool calls into guard.ts, exactly the way
// Claude Code would (JSON on stdin), and prints what the guard decided.
// You don't need Claude Code installed to run this. No key, no spend.
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

type Call = {
  tool_name: string;
  tool_input: { command?: string; file_path?: string };
};

const calls: Call[] = JSON.parse(readFileSync("calls.json", "utf8"));

for (const call of calls) {
  const run = spawnSync(process.execPath, ["--import", "tsx", "guard.ts"], {
    input: JSON.stringify(call),
    encoding: "utf8",
  });
  const target = call.tool_input.command ?? call.tool_input.file_path;
  if (run.status === 2) {
    console.log(`BLOCK ${target}`);
    console.log(`  ${run.stderr.trim()}`);
  } else {
    console.log(`ALLOW ${target}`);
  }
}
