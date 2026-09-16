// Model id and budgets live here, never in the loop.
// Take the model id from the models overview page:
// https://platform.claude.com/docs/en/about-claude/models/overview
export const MODEL =
  process.env.CLAUDE_MODEL ?? "set CLAUDE_MODEL in .env";
export const MAX_TURNS = 6;
export const MAX_TOKENS = 1024;
