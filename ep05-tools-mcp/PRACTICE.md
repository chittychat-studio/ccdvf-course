# EP 05 practice: tools and MCP

Two parts. **Hands-on exercises** you run against `server.ts`, then
**practice questions** in the exam's scenario style. Answers are folded under
each item, so try it first.

Every question here is original, written for this series, and is not drawn from
any real exam.

**Cost:** every exercise here is **FREE**. Nothing calls the Anthropic API.

---

## Part 1: hands-on

### 1. Recreate the bug from the cold open

In `server.ts`, change **both** tool descriptions to:

```ts
description: "Use this for account questions.",
```

Run `npm run try` and read step 1 of the output. You are now the model: a
customer asks *What's my balance?* Which drawer would you open?

<details><summary>What this shows</summary>

You can't tell. The two labels are identical, so the choice comes down to the
tool name and luck. That is the refund from the cold open. Nothing in the code
was broken: the label was the bug. Put the three-part descriptions back.

</details>

### 2. Make the error useless, then fix it

Change `missing()` so it returns just `"failed"`, and remove `isError: true`.
Run `npm run try`. What does step 4 print for `meera` now?

<details><summary>What this shows</summary>

`get_balance -> failed`, with no `ERROR`. A client, or Claude, now sees an
ordinary result whose text is "failed". It can't tell it was an error, and it
has no idea what to do next, so the usual next move is to guess or retry the
same call. `isError` says it failed. The sentence says what to try instead.
Put both back.

</details>

### 3. Add a third drawer

Add a tool `get_last_payment` that returns the date of an account's last
payment. Before you type, write its three-part label.

<details><summary>One good answer</summary>

```ts
description:
  "Read the date of one account's last payment. " +
  "Returns a date. " +
  "Never use this for balances or refunds.",
```

The exclusion is the part people skip, and it matters most when a new drawer
sits next to one that sounds similar. Add `annotations: { readOnlyHint: true }`,
then call it from `try.ts` to prove it works.

</details>

### 4. Two drawers or one?

You're asked for `get_balance_gbp` and `get_balance_eur`. Their labels would
have to grow to keep them apart. What do you build instead?

<details><summary>Answer</summary>

One drawer, with a type to choose: `get_balance` with a `currency` input,
limited to the values you support (`z.enum(["GBP", "EUR"])`). Near-duplicate
tools with ever-longer labels are the sign to merge.

</details>

### 5. Resource, prompt or tool? (no code)

For each, say whether it should be a **tool**, a **resource** or a **prompt**.

| # | Thing |
|---|---|
| a | The refund policy text, which the app attaches when a ticket mentions refunds |
| b | "Triage this ticket", which a support agent picks from a menu |
| c | Look up an order's shipping status |

<details><summary>Answers</summary>

- **a. Resource.** Read-only content the application decides to include.
- **b. Prompt.** A template the user chooses, often as a slash command.
- **c. Tool.** The model decides to call it, with arguments, when it needs to.

</details>

### 6. Your one move this week

Take one tool or function your team already exposes to an AI assistant. Rewrite
its description with all three parts, including one sentence that starts
*Never use this*. Then check whether any two of your tools now read the same.

---

## Part 2: practice questions

### Q1. The one from the episode

One app has a ticket lookup tool. Three more teams want the same lookup in
their own apps. What's the best move?

- A. Copy the tool into every app
- B. Wrap it as an MCP server they all connect to
- C. Write a skill that describes the lookup
- D. Paste the whole ticket database into the system prompt

<details><summary>Answer</summary>

**B.** One server, many clients. A gives you four copies to keep in step. C
teaches *how* to do something, but gives nobody the connection. D fills the
context on every single call.

</details>

### Q2. The wrong drawer

An agent has `get_customer` and `update_customer`. Both descriptions say
"Use for customer records." It sometimes calls `update_customer` when a user
only asks a question. What's the best first fix?

- A. Remove `update_customer`
- B. Give each tool a specific description, including when not to use it
- C. Add "be careful" to the system prompt
- D. Switch to a larger model

<details><summary>Answer</summary>

**B.** The model only knows what the description tells it, and these two read
the same. A removes a capability you need. C is vague and doesn't tell the model
which tool is which. D doesn't fix identical labels.

</details>

### Q3. When a tool fails

A lookup tool can't find the account and returns the text `failed`. The model
keeps retrying the same call. What change helps most?

- A. Return an empty result so the model moves on
- B. Mark the result as an error, and say what went wrong and what to try next
- C. Add retries with backoff inside the tool
- D. Raise the model's temperature

<details><summary>Answer</summary>

**B.** An error the model can act on (*No account by that name. Ask for the
name on the account.*) gives it a next step. A hides the failure. C helps with
flaky networks, not with an account that doesn't exist. D changes randomness,
not information.

</details>

### Q4. The dangerous drawer

A support agent can issue refunds through a tool. You want the model to be
able to start a refund, but never to complete one on its own. What's the best
design?

- A. Tell the model in the system prompt never to refund more than a set amount
- B. Make the tool file a request that a person approves outside the conversation
- C. Remove the tool and ask users to email finance
- D. Give the tool a description that says "use carefully"

<details><summary>Answer</summary>

**B.** The safety sits in the code, not in a sentence the model reads. A and D
still let the model move money if it misreads. C throws away the useful part.

</details>

### Q5. Too many servers

A developer connects every MCP server they can find. Tool choice gets worse and
responses slow down, even for simple questions. What's the most likely cause?

- A. MCP servers share one network connection
- B. Every connected server's tool descriptions take up space in the context
- C. MCP only allows five servers
- D. The model can't use tools from more than one server

<details><summary>Answer</summary>

**B.** Each connected server adds its tool descriptions to what the model reads,
before anyone says hello. More, and more similar, labels make the choice harder.
Connect what you use. A, C and D aren't how MCP works.

</details>

### Q6. Tool, server or skill?

Your team has a long checklist for writing release notes: tone, sections, what
to leave out. Nothing needs to be looked up. What fits best?

- A. A tool
- B. An MCP server
- C. A skill
- D. A bigger system prompt on every call

<details><summary>Answer</summary>

**C.** This is know-how, not a connection. A skill loads its instructions when
the task needs them. A and B are for reaching systems. D pays for the checklist
on every call, including the ones that have nothing to do with release notes.

</details>
