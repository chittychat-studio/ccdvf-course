# CCDV-F EP 05 companion code

**Tools and MCP.** The support desk from the episode, with its drawers
labelled properly and packed as a small MCP server. Runnable code for
[EP 05 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Clone it, run it, break it on purpose. Then work through
[`PRACTICE.md`](PRACTICE.md).

## What's here

| File | What it is | Calls the API? |
|---|---|---|
| `server.ts` | The MCP server built in the episode: two tools, one resource, one prompt | **No** |
| `try.ts` | A real MCP client that starts the server and calls everything in it | **No.** No key, no spend |
| `PRACTICE.md` | Hands-on exercises and original practice questions, answers included | None of the exercises need a key |

Nothing in this folder needs an Anthropic API key. `try.ts` plays the part
Claude Code or Claude Desktop would play, so you can see exactly what a client
sees.

## Setup

You need Node 20 or newer.

```
npm install
npm run try
```

What it should print:

```
1. What's in the cabinet (tools/list)
   get_balance: Read one account's balance. Returns a number. Never use this to move money.
   request_refund: File a refund for a person to approve. Returns a request. Never use this for balances.
2. A resource (resources/read), no tool call
   Refunds within thirty days. A person approves every refund.
3. A prompt (prompts/get), picked by the user
   1 message, starts: Read the refund policy first. Then sort ...
4. Tool calls (tools/call)
   get_balance -> asha: 2450
   get_balance -> ERROR No account "meera". Ask for the name on the account.
   request_refund -> Queued for approval: asha, 500
```

`npm run typecheck` runs the TypeScript compiler with no output files.

## The four moves, in the file

| Move | Where it is in `server.ts` |
|---|---|
| **The label** | Each tool's `description`: what it does, what comes back, and when *not* to use it |
| **The break** | `get_balance` returns `isError: true` with a sentence that says what to try next |
| **The locked drawer** | `request_refund` never moves money. It files a request a person approves |
| **Borrow** | The whole file is an MCP server. Any MCP client can use it without a rewrite |

The last three lines of `try.ts`'s output are the ones shown on screen in the
episode.

## Plug it into a real client (optional)

These steps change between releases, so check the linked docs first.

- **Claude Code:** add it as a local stdio server. See
  [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp).
  From this folder:
  `claude mcp add --transport stdio support-desk -- npx tsx server.ts`
- **Claude Desktop:** add it to the app's MCP server config as a local
  command. See the [MCP quickstart for users](https://modelcontextprotocol.io/quickstart/user).

Using it from a Claude client uses your normal plan or account. It does not
need an API key.

## What the exam cares about

- Claude never runs a tool. It reads the descriptions and asks. Your code runs it.
- A good description says what the tool does, what comes back, and when not to use it.
- An error the model can act on beats a bare "failed". Mark it as an error.
- A tool that can do damage should ask, not act. A person says yes.
- MCP packs tools, resources and prompts so any MCP client can use them.
- Tools are picked by the model, resources by the app, prompts by the user.
- Every connected server's tools take up room in the context. Connect what you use.

## Sources

Current at the time of writing. Check them before you build on any of this.

- [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

Independent study material. Not affiliated with or endorsed by Anthropic. Every
practice question here is original and is not drawn from any real exam. All
account data in `server.ts` is made up.
