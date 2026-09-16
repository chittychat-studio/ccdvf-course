// Human in the loop: pause before any send.
import * as readline from "node:readline/promises";
import { stdin, stdout } from "node:process";
import type { ToolUseBlock } from
  "@anthropic-ai/sdk/resources/messages";

type Call = ToolUseBlock;
const GATE_OFF = process.env.GATE === "off";

const SENDS = new Set(["page_owner"]);
export async function gate(block: Call) {
  if (!SENDS.has(block.name)) return true;
  if (GATE_OFF) return noGate();
  const answer = await ask(
    `approve ${block.name}? [y/N] `);
  return answer.trim() === "y";
}

function noGate() {
  console.log("gate off: sent with no human");
  return true;
}

async function ask(prompt: string) {
  const rl = readline.createInterface({
    input: stdin,
    output: stdout,
  });
  const answer = await rl.question(prompt);
  rl.close();
  return answer;
}
