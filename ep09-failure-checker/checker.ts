// checker.ts - CCDV-F EP 09 companion.
// Reads recorded traces. For each run
// that failed, it prints the step
// that broke, code or model, and what
// to do next. It never calls the API.
// No key, no spend.
import { readFileSync } from "node:fs";

// One step of a run, as a trace
// records it. owner says who owns it:
// "code" is your integration layer,
// "model" is the model's own output.
type Step = {
  name: string;
  owner: "code" | "model";
  ok: boolean;
  status?: number; // HTTP status
  stop?: string; // stop_reason
  note?: string;
};
type Trace = { id: string; steps: Step[] };

// Time can fix these. Retry them.
const RETRY = new Set([429, 529,
  500, 502, 503, 504]);

// Retry or fail fast?
function next(s: Step): string {
  if (s.stop === "refusal")
    return "FAIL FAST, refusal";
  if (RETRY.has(s.status ?? 0))
    return "RETRY, back off";
  if (s.owner === "model")
    return "FIX PROMPT, RE-EVAL";
  return "FAIL FAST, fix input";
}

const say = (...parts: string[]) =>
  console.log(parts.join(" "));
const firstFail = (t: Trace) =>
  t.steps.find((s) => !s.ok);

const file = process.argv[2] ??
  "traces.json";
const traces: Trace[] = JSON.parse(
  readFileSync(file, "utf8"));

for (const t of traces) {
  const bad = firstFail(t);
  if (!bad) {
    say(t.id, "PASS");
    continue;
  }
  say(t.id, bad.name.padEnd(6),
    bad.owner.padEnd(5), next(bad));
}
