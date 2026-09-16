# EP 02 - Agents and Workflows (CCDV-F, Domain 1)

Companion code for CorporateChittyChat's CCDV-F exam-prep episode 2. Independent
study material. Not affiliated with, endorsed by, or approved by Anthropic.

One agent loop in TypeScript, written against the Messages API with the Anthropic
TypeScript SDK, wired the way the episode's checklist says:

| checklist item | where |
|---|---|
| tools registered, minimum set, each with a "do not use" | `tools.ts` |
| system prompt scoped to the job and the two tools | `loop.ts` (`system`) |
| tool-use loop: run every `tool_use`, return every `tool_result` paired by id | `loop.ts` (the `for` loop) |
| human-in-the-loop gate before a send | `gate.ts` |
| exit condition: any non tool_use stop reason, or `MAX_TURNS` | `loop.ts` |

Nothing real is paged. `page_owner` prints a line.

## Run

```
npm install
cp .env.example .env   # fill ANTHROPIC_API_KEY and CLAUDE_MODEL
npm run loop           # with the gate: you are asked before any page
npm run loop:nogate    # gate off: watch what the loop does on its own
```

`incident.json` is the episode's incident: a test service flagged critical. Run
it both ways and post the log line the no-gate run prints, in the episode comments.

Model ids, parameters and stop reasons change. Check the docs before relying on any
of this in production:

- Tool use overview: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
- Handling tool calls: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls
- Agent SDK: https://code.claude.com/docs/en/agent-sdk/overview
- Managed Agents: https://platform.claude.com/docs/en/managed-agents/overview
- Context windows: https://platform.claude.com/docs/en/build-with-claude/context-windows

Every practice question in the episode is original and is not drawn from any real exam.
