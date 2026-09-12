from anthropic import Anthropic
from config import MODEL, STYLE_GUIDE

client = Anthropic()
ticket = open("ticket.txt").read()
r = client.messages.count_tokens(
    model=MODEL, system=STYLE_GUIDE,
    messages=[{"role": "user",
               "content": ticket}],
)
print("input tokens", r.input_tokens)
