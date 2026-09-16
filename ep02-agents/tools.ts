// EP 02 companion: two tools, nothing wider.
// Each description says when NOT to use it.
import type Anthropic from "@anthropic-ai/sdk";

export const lookupOwner: Anthropic.Tool = {
  name: "lookup_owner",
  description:
    "Find the on call owner of one service " +
    "by service name. Do not use it to " +
    "page anyone.",
  input_schema: {
    type: "object",
    properties: { service: { type: "string" } },
    required: ["service"],
  },
};

export const pageOwner: Anthropic.Tool = {
  name: "page_owner",
  description:
    "Page one owner about one incident. " +
    "Use only when it is critical. " +
    "Do not use it to ask questions.",
  input_schema: {
    type: "object",
    properties: {
      owner: { type: "string" },
      summary: { type: "string" },
    },
    required: ["owner", "summary"],
  },
};

export const tools = [lookupOwner, pageOwner];

// Fake executors. Nothing real is paged.
const OWNERS: Record<string, string> = {
  "checkout-test": "priya",
  "payments": "dev-oncall",
};

export function runTool(name: string, input: any) {
  if (name === "lookup_owner") {
    const who = OWNERS[input.service] ?? "unknown";
    return `owner of ${input.service}: ${who}`;
  }
  if (name === "page_owner") {
    console.log(`PAGED ${input.owner}: ${input.summary}`);
    return "paged";
  }
  return `unknown tool: ${name}`;
}
