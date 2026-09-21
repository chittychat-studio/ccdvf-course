# CCDV-F EP 03 companion code

**Applications and Integration, part one: API mechanics.** The four moves from the
episode, one file each - Messages, Streaming, Images, Batches. Runnable code for
[EP 03 of the CCDV-F Exam Prep series](https://www.youtube.com/@Corporatechittychat).

Everything here is the code from the episode, plus the bits that would not fit
on screen. Clone it, run it, break it on purpose.

## Setup

```
pip install -r requirements.txt
cp .env.example .env        # put your key in it
```

Get a key from [the Claude Console](https://console.anthropic.com/). Every
script here bills your account when it calls the API, except `image_cost.py`,
which does arithmetic locally and never calls anything.

## The five files

### `messages_basics.py` - the Messages API itself

```
python messages_basics.py
python messages_basics.py --show-growth
```

Three things a request needs: `model`, `max_tokens`, `messages`. Two things people
get wrong, both demonstrated in the file:

1. **The system prompt is not a message.** It is its own top-level `system`
   parameter, sitting beside `messages`. This is the most common mistake when
   porting from a chat-completions-shaped API.
2. **The API is stateless.** It stores nothing between calls, so you resend the
   whole conversation every turn. `--show-growth` runs three turns so you can
   watch input tokens climb while you type less. That is also why one corrupted
   turn in your history keeps breaking every request after it - see
   `stream_handler.py`.

`content` is a **list of blocks**, not a string. Text is one block type among
several (image, document, tool_use, tool_result, thinking).

Every `stop_reason`, and what it means:

| `stop_reason` | Meaning |
|---|---|
| `end_turn` | Finished naturally |
| `max_tokens` | You cut it off |
| `stop_sequence` | Hit one of your stop sequences |
| `tool_use` | It wants to call a tool |
| `pause_turn` | A long-running turn paused; continue it |
| `refusal` | The model declined |
| `model_context_window_exceeded` | Generation hit the context window |

### `stream_handler.py` - the handler built in the episode

Assembles a streamed message from the event series, and refuses to hand you
anything from an incomplete stream.

```
python stream_handler.py
python stream_handler.py --simulate-drop
```

`--simulate-drop` cuts the stream mid tool call, which is the whole point.
Watch the guard refuse to build an assistant turn, and watch the conversation
history stay untouched. That is the difference between a cosmetic glitch and a
corrupted conversation.

The six events, and what the handler does with each:

| Event | What it means | What the handler does |
|---|---|---|
| `message_start` | A message is beginning | Empty the block list |
| `content_block_start` | A block is opening | Make a slot at that index |
| `content_block_delta` | A piece of that block | Append it, interpret nothing |
| `content_block_stop` | That block is finished | **Now** parse a tool call's input |
| `message_delta` | Stop reason and final usage | Record the stop reason |
| `message_stop` | The whole message is done | Mark the turn safe to use |

`ping` and `error` events also exist. A `ping` is a keep-alive and recovers
nothing, which is why there is no handler for it.

**The rule:** a `tool_use` block's `input` arrives as a partial JSON string
spread across many `input_json_delta` events. It is not valid JSON until
`content_block_stop`. Parse early and you crash; run the tool early and you run
it with half its arguments.

### `image_cost.py` - what an image costs before Claude reads your prompt

No API call, no key needed.

```
python image_cost.py 1000 1000
python image_cost.py --file screenshot.png --long-edge 1568 --token-cap 1568
python image_cost.py 4000 3000 --budget 800
```

Claude views an image in 28x28 pixel patches, one visual token per patch:

```
tokens = ceil(width / 28) * ceil(height / 28)
```

Two ceilings apply, not one: a longest-edge limit and a visual-token limit, both
per model tier. Over either, the image is downscaled first, so the sum runs on
the scaled size. `--budget` gives you a resize target for an over-budget
pipeline, which is usually a ten-minute fix before deployment and a much longer
one after.

Per-tier limits change between model generations. Look yours up in
[the Vision docs](https://platform.claude.com/docs/en/build-with-claude/vision)
rather than trusting a number from a video, including this one.

### `send_document.py` - PDFs

```
python send_document.py contract.pdf "List every payment obligation."
```

A PDF is a `document` block, not an `image` block. Same three source options as
an image: `base64`, `url`, or a Files API `file_id`. No required `name` field;
`title` and `context` are optional. Reach for `file_id` the moment the same
document is sent more than once.

### `batch_run.py` - the Message Batches API

```
python batch_run.py submit records.jsonl
python batch_run.py poll   msgbatch_xxxxxxxx
python batch_run.py fetch  msgbatch_xxxxxxxx --out results.jsonl
```

`records.jsonl` is five sample support messages so you can run the whole loop
for a few cents.

Two things the episode does not have room for, and both bite:

1. **Results do not come back in submission order.** Join on `custom_id`, never
   on position.
2. **Every result has a `type`**, one of `succeeded`, `errored`, `canceled`, or
   `expired`. Only `succeeded` is billed. Handle all four.

`processing_status` on the batch itself is one of `in_progress`, `canceling`,
or `ended`.

## Which API, per workload

| Workload | Pattern | Why |
|---|---|---|
| User uploads a photo, wants a classification now | Synchronous | Someone is waiting |
| Nightly job over thousands of records | Batches | Latency is free here, cost is not |
| Eval run over a fixed test set | Batches | Offline, no real-time requirement |
| Chatbot reply | Synchronous | Someone is very much waiting |
| Long answer in a user-facing UI | Streaming | Removes the blank-screen wait |

Getting this one backwards is the failure that passes every test and feels
broken in production.

## Sources

Current at the time of writing. Batch limits, pricing and per-tier image caps
all change. Verify before you design around them.

- [Streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Vision, resolution and token cost](https://platform.claude.com/docs/en/build-with-claude/vision)
- [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support)
- [Messages API](https://platform.claude.com/docs/en/api/messages)
- [Message Batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing)

## Licence

MIT. Use it however you like.
