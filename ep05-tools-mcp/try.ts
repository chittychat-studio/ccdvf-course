/**
 * EP 05: talk to server.ts the way any MCP client does. No API key, no spend.
 *
 * This file plays the part Claude Code or Claude Desktop would play: it
 * starts the server as a subprocess over stdio, asks what's inside, and
 * calls the tools directly. In a real app, Claude would pick which tool to
 * call by reading the descriptions printed in step one.
 *
 * Run:  npm run try
 */
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const client = new Client({ name: "ep05-try", version: "1.0.0" });
await client.connect(new StdioClientTransport({
  command: process.execPath,
  args: ["--import", "tsx", "server.ts"],
}));

const text = (r: any) => r.content.map((c: any) => c.text).join(" ");

console.log("1. What's in the cabinet (tools/list)");
for (const t of (await client.listTools()).tools) {
  console.log(`   ${t.name}: ${t.description}`);
}

console.log("2. A resource (resources/read), no tool call");
const policy = await client.readResource({ uri: "policy://refunds" });
console.log(`   ${(policy.contents[0] as any).text}`);

console.log("3. A prompt (prompts/get), picked by the user");
const p = await client.getPrompt({ name: "triage", arguments: { ticket: "Charged twice." } });
console.log(`   ${p.messages.length} message, starts: ${(p.messages[0].content as any).text.slice(0, 40)}...`);

console.log("4. Tool calls (tools/call)");
for (const [name, args] of [
  ["get_balance", { account: "asha" }],
  ["get_balance", { account: "meera" }],
  ["request_refund", { account: "asha", amount: 500 }],
] as const) {
  const r: any = await client.callTool({ name, arguments: args });
  console.log(`   ${name} -> ${r.isError ? "ERROR " : ""}${text(r)}`);
}

await client.close();
