# EP 09 practice: evals, test levels, traces and recovery

Two parts. **Hands-on exercises** you run against `checker.ts`, then **practice
questions** in the exam's scenario style. Answers are folded under each item, so
try it first.

Every question here is original, written for this series, and is not drawn from
any real exam.

**Cost:** every exercise here is **FREE**. Nothing calls the Anthropic API.

---

## Part 1: hands-on

### 1. The service is overloaded

Change `c1`'s status from `429` to `529` and run it again.

<details><summary>What this shows</summary>

Still `RETRY, back off`. Overloaded is Anthropic-side load, not your rate limit,
but time fixes both, so both retry.

</details>

### 2. A permissions error

Change `c2`'s status from `400` to `403`.

<details><summary>What this shows</summary>

Still `FAIL FAST, fix input`. A key without permission fails the same way every
time. Waiting changes nothing, so retrying only burns the retry budget.

</details>

### 3. Two failures in one run

Add a second failed step after `c1`'s failed call, say a `check` owned by
the `model`. What does the checker report?

<details><summary>What this shows</summary>

Only the first one, the rate limit. Everything after the first failure ran on
bad input, so fix the first failed step before you trust anything later in the
trace.

</details>

### 4. Move the refusal check

In `next`, move the `refusal` check below the `owner === "model"` check. Run it.
What does `c5` say now, and why is the original order right?

<details><summary>What this shows</summary>

`c5` becomes `FIX PROMPT, RE-EVAL`. A refusal is the model's content decision,
not a quality bug, and it arrives as a normal success. It needs its own branch,
checked first: raise it, log it, and don't retry it or treat it as valid output.

</details>

### 5. Write your own trace

Record five runs of a feature you've built, as steps with an `owner` and `ok`.
Run the checker on them.

<details><summary>What this shows</summary>

If you can't say whether a step is your code or the model, the trace is missing a boundary. Split
the step until each one belongs to your code or to the model's output.

</details>

---

## Part 2: practice questions

### Q1

A summariser must return valid JSON with an `owners` field. You want a check that
runs on every commit, for free. Which grader?

A. An LLM judge with a rubric
B. An exact string match against a reference answer
C. A code check that parses the JSON and requires `owners`
D. A human review of ten samples

<details><summary>Answer</summary>

**C.** The rule is structural, so code can decide it, at no cost per case. A
costs a model call per case and adds noise. B fails every valid reordering. D
doesn't scale to every commit.

</details>

### Q2

Your retrieval step passes its unit tests. So does the model call. End to end,
answers cite the wrong document. Which test do you add first?

A. More end-to-end tests
B. An integration test on the handover from retrieval into the model call
C. A unit test for the prompt template
D. A load test

<details><summary>Answer</summary>

**B.** Both sides pass alone, so the break is at the seam. A confirms the failure
again without telling you where it is.

</details>

### Q3

Your LLM judge scores almost every answer between five and seven, whatever the
quality. What do you change first?

A. Switch to a larger judge model
B. Ask for strengths, weaknesses and reasoning before the score, then check it against human-labelled cases
C. Average three judge runs
D. Drop the judge and use exact match

<details><summary>Answer</summary>

**B.** A score with no reasoning drifts to a safe middle. Reasoning first
anchors it, and calibration against human labels tells you whether you can
trust it.

</details>

### Q4

You use an official SDK, and you've wrapped every call in your own retry loop
of five attempts. At peak, rate-limit errors get worse. Why?

A. The SDK doesn't retry anything
B. Two retry layers multiply the attempts against the same limit
C. Rate limits are terminal
D. The retry-after header is always missing

<details><summary>Answer</summary>

**B.** The SDKs already retry transient failures with backoff. Pick one place
for retries: let the SDK handle transient cases, or turn its retries down and
own the whole path.

</details>
