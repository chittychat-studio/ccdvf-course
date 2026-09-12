from anthropic import Anthropic
from config import MODEL, STYLE_GUIDE, MAX_OUT

client = Anthropic()
ticket = open("ticket.txt").read()
system = [{
    "type": "text",
    "text": STYLE_GUIDE,
    "cache_control": {"type": "ephemeral"},
}]
resp = client.messages.create(
    model=MODEL, max_tokens=MAX_OUT,
    system=system,
    messages=[{"role": "user", "content": ticket}],
)
u = resp.usage
print("cache write", u.cache_creation_input_tokens)
print("cache read ", u.cache_read_input_tokens)
print("input      ", u.input_tokens)
