# Fill these on the day you run the code. They are deliberately blank here:
# model ids and prices change, and a stale number in a repo is worse than none.
#   MODEL     -> a current model id from the models overview page
#   RATE_IN   -> input price per token  (per-million price / 1e6)
#   RATE_OUT  -> output price per token (per-million price / 1e6)
MODEL = "REPLACE_WITH_CURRENT_MODEL_ID"
MAX_OUT = 64
RATE_IN = 0.0 / 1_000_000
RATE_OUT = 0.0 / 1_000_000
BUDGET_PER_TICKET = 0.01

# The stable prefix that is the same on every request. It must be LONGER than
# the model's minimum cacheable prompt (the caching docs list a per-model
# minimum) or nothing is cached and cache_creation_input_tokens stays at zero,
# silently.
STYLE_GUIDE = open("style_guide.txt").read()
