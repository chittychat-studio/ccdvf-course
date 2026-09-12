# EP 01 — Model Selection and Optimization: count, price, cache

Companion code for CorporateChittyChat's CCDV-F exam-prep series, episode one.
Three small files that exercise the blueprint's Domain 5 task statements:

| file | what it shows | blueprint |
|---|---|---|
| `count.py` | count input tokens for a request before sending it (free endpoint) | 5.1 tokens and context, 5.4 token budgeting |
| `price.py` | turn a response's usage block into a per-ticket cost and refuse past a budget | 5.4 cost modelling |
| `cache.py` | mark the stable system prompt with `cache_control` and read the cache fields back | 5.4 prompt caching |

## Run

    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env            # put your key in .env, never in code
    # edit config.py: a current model id, your rates from the pricing page
    python count.py
    python cache.py && python cache.py   # second run inside the cache window

`price.py` is a helper you call from your own request loop (`price(resp, ticket_id)`).

## Notes

- The model id and the per-token rates are deliberately not in this repo. They change.
  Read them from the models overview and the pricing page on the day you run this.
- The style guide must be longer than the per-model cache minimum or nothing is cached
  (no error is raised — you just see zero in `cache_creation_input_tokens`).
- Tested on the model family named in the episode description; behaviour can change
  between releases, so pin the id you test against.
- Not affiliated with or endorsed by Anthropic. Independent study material.
