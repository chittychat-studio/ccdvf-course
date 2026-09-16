// EP 02 companion: the agent loop, in TypeScript.
// Register tools, scope the prompt, handle the loop,
// gate the send, define the exit.
import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUseBlock } from
  "@anthropic-ai/sdk/resources/messages";
import { readFileSync } from "node:fs";
import { tools, runTool } from "./tools";
import { gate } from "./gate";
import { MODEL, MAX_TURNS, MAX_TOKENS } from "./config";

const client = new Anthropic();
const incident = readFileSync("incident.json", "utf8");

const system =
  "You triage one incident. Look up the " +
  "owner, then page them only if the " +
  "service is critical. You have two " +
  "tools and nothing else.";
const messages: MessageParam[] = [
  { role: "user", content: incident },
];

for (let t = 1; t <= MAX_TURNS; t++) {
  const res = await client.messages.create({
    model: MODEL,
    max_tokens: MAX_TOKENS,
    system,
    tools,
    messages,
  });
  messages.push({
    role: "assistant",
    content: res.content,
  });
  const results: any[] = [];
  if (done(res, t)) break;
  for (const block of res.content) {
    if (block.type !== "tool_use") continue;
    const out = await handle(block);
    results.push({ type: "tool_result",
      tool_use_id: block.id, content: out,
    });
  }
  messages.push({ role: "user", content: results });
}

// Gate the send, then run the tool.
async function handle(block: ToolUseBlock) {
  const ok = await gate(block);
  if (!ok) return "declined by a human, not sent";
  return runTool(block.name, block.input);
}

// Exit: a stop reason other than tool_use,
// or the turn cap, whichever comes first.
type Res = Anthropic.Message;
function done(res: Res, t: number) {
  if (res.stop_reason !== "tool_use") {
    console.log(`exit: ${res.stop_reason}`);
    return true;
  }
  if (t < MAX_TURNS) return false;
  console.log("exit: max turns reached");
  return true;
}
