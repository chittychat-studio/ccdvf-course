# EP 08 practice: requirements, the life cycle and its gates

Two parts. **Hands-on exercises** you run against `gate_check.py`, then
**practice questions** in the exam's scenario style. Answers are folded under
each item, so try it first.

Every question here is original, written for this series, and is not drawn from
any real exam.

**Cost:** every exercise here is **FREE**. Nothing calls the Anthropic API.

---

## Part 1: hands-on

### 1. Rewrite the vague requirement

In `fixtures/ravi-plan/requirements.json`, rewrite R1 so a test could check it.
Run the checker again.

<details><summary>What this shows</summary>

"Answer customers faster" is a business wish. "Draft a first reply within one
working minute of a ticket arriving" is a requirement: an eval can measure it.

</details>

### 2. Delete an infrastructure answer

Remove `identity` from the record and run the checker.

<details><summary>What this shows</summary>

It prints `FLAG missing: identity`. Nobody states the infrastructure
requirements in the business problem. You have to ask for all four.

</details>

### 3. Move the platform

Change `platform.region` in `release.json` to `india`. What changes, and which
gate did you just clear?

<details><summary>What this shows</summary>

The residency flag goes. That was the design gate: the platform has to meet the
residency rule before the build starts. The rule, not familiarity, picked the
platform.

</details>

### 4. Ship a model you didn't test

Change `model` so it no longer matches `tested`.

<details><summary>What this shows</summary>

`FLAG model: untested`. Pin the exact model you tested, and keep the old version
so you can roll back.

</details>

### 5. Add a gate of your own

Add a check that flags a release with no `prompt_edition`.

<details><summary>What this shows</summary>

A prompt is versioned with the code. A release that can't say which prompt
edition it ships can't be rolled back cleanly.

</details>

---

## Part 2: practice questions

### Q1

A product owner writes "the assistant should be easy to use and respond
quickly". What's the best next step?

- A. Start building and tune it later
- B. Turn it into checkable functional requirements, and ask the latency question
- C. Pick the fastest model
- D. Add "respond quickly" to the system prompt

<details><summary>Answer</summary>

**B.** A vague goal can't be designed against or verified. Checkable
requirements become eval lines, and "quickly" becomes a latency requirement,
measured where the user sits.

</details>

### Q2

A new prompt edition scores better in your offline tests. What should the
deploy step do?

- A. Replace the old edition for all traffic
- B. Send it a small share of traffic, compare against the pinned baseline, then promote or roll back
- C. Ship it and delete the old edition
- D. Switch to the model alias so it stays current

<details><summary>Answer</summary>

**B.** Promotion goes through the eval against the baseline, and the old version
stays available for rollback.

</details>

### Q3

A Claude Code task fetches a customer's web page, and the next component passes
that text straight into its instructions. What's wrong?

- A. Nothing, the page came from the customer
- B. Fetched content crossed a trust boundary and must be treated as data, not instructions
- C. The model should be pinned
- D. The task needs a larger context window

<details><summary>Answer</summary>

**B.** Every seam between components is a trust boundary. Content fetched by one
part is untrusted when it reaches the next.

</details>

### Q4

Every component in an app is tightly scoped except one MCP server, which holds
write access to the whole customer system. How safe is the app?

- A. Mostly safe, since most parts are scoped
- B. Only as safe as that one server
- C. Safe, if the prompts say not to write
- D. Safe, if it runs on the customer's cloud

<details><summary>Answer</summary>

**B.** The app is only as contained as its most privileged seam. Scope that
server to the access its job needs.

</details>
