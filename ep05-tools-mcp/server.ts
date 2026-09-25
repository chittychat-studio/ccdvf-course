/**
 * EP 05: a small support-desk MCP server, over stdio.
 *
 * Everything from the episode, in one file:
 *
 *   Move one, the label.   Every tool says what it does, what comes back,
 *                          and when NOT to use it. Claude only ever reads
 *                          the label, so the label is the whole interface.
 *   Move two, the break.   A tool that fails says so (isError), in a sentence
 *                          that tells Claude what to try next. The refund tool
 *                          never moves money: it files a request that a
 *                          person approves. The dangerous drawer stays locked.
 *   Move three, borrow.    The same drawers, packed as an MCP server, so any
 *                          MCP client (Claude Code, Claude Desktop, your own
 *                          app) can use them without rewriting anything.
 *                          Tools, one resource, one prompt.
 *
 * Lines shown on screen in the episode are copied from this file verbatim,
 * which is why some of them are split more than you'd normally split them.
 *
 * No Anthropic API key is needed to run or try this. `npm run try` calls it
 * from a real MCP client over stdio.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Fictional data. Nothing here is a real account.
const ACCOUNTS: Record<string, number> = { asha: 2450, ravi: 0 };
const REFUND_QUEUE: { account: string; amount: number }[] = [];

const server = new McpServer({ name: "support-desk", version: "1.0.0" });
const text = (t: string) => [{ type: "text" as const, text: t }];

// ---- Move one: the label ------------------------------------------------
// The cold open's bug: both tools said "Use this for account questions".
// Each label below has three parts: what it does, what comes back, and
// when not to use it. The last part is the exclusion.
server.registerTool("get_balance", {
  description:
    "Read one account's balance. " +
    "Returns a number. " +
    "Never use this to move money.",
  inputSchema: { account: z.string() },
  annotations: { readOnlyHint: true },
}, async ({ account }) => {
  const balance = ACCOUNTS[account.toLowerCase()];
  // ---- Move two: the break ----------------------------------------------
  // "failed" teaches Claude nothing. Mark it as an error, say what went
  // wrong, and say what to try next.
  if (balance === undefined) return {
    isError: true,
    content: text(missing(account)),
  };
  return { content: text(`${account}: ${balance}`) };
});

const missing = (a: string) =>
  `No account "${a}". ` +
  "Ask for the name on the account.";

server.registerTool("request_refund", {
  description:
    "File a refund for a person to " +
    "approve. Returns a request. " +
    "Never use this for balances.",
  inputSchema: { account: z.string(), amount: z.number() },
  annotations: { destructiveHint: true },
}, async ({ account, amount }) => {
  // The locked drawer. This tool never pays anyone. It files a request,
  // and a person approves it outside the conversation.
  REFUND_QUEUE.push({ account, amount });
  return { content: text(`Queued for approval: ${account}, ${amount}`) };
});

// ---- Move three: resources and prompts ----------------------------------
// a resource: read-only, no tool call
server.registerResource(
  "refund-policy", "policy://refunds",
  { description: "The refund policy.", mimeType: "text/plain" },
  async (uri) => ({
    contents: [{ uri: uri.href,
      text: "Refunds within thirty days. A person approves every refund." }],
  }),
);

// a prompt the user picks
server.registerPrompt("triage", {
  description: "Sort one ticket.",
  argsSchema: { ticket: z.string() },
}, ({ ticket }) => ({
  messages: [{ role: "user", content: { type: "text",
    text: "Read the refund policy first. Then sort this ticket, " +
      `and never promise a refund yourself.\n<ticket>${ticket}</ticket>` } }],
}));

// Local server: stdio. The client starts this file as a subprocess and
// talks to it over standard input and output. A shared, remote server
// would use Streamable HTTP instead. The tools above would not change.
const io = new StdioServerTransport();
await server.connect(io);
