"""EP 03, move three: what an image costs you before Claude reads your prompt.

Claude views an image in 28x28 pixel patches. Each patch is one visual token:

    tokens = ceil(width / 28) * ceil(height / 28)

Each model also caps the longest edge and the visual-token count. Over the cap,
the image is downscaled FIRST, so the formula runs on the scaled size. Those
per-tier caps change between model generations. Look them up at build time:
https://platform.claude.com/docs/en/build-with-claude/vision

Run:  python image_cost.py 1920 1080
      python image_cost.py --file screenshot.png
      python image_cost.py --file screenshot.png --budget 800
"""

from __future__ import annotations

import argparse
import math

PATCH = 28


def visual_tokens(width: int, height: int) -> int:
    return math.ceil(width / PATCH) * math.ceil(height / PATCH)


def downscale_for_tier(
    width: int, height: int, max_long_edge: int, max_visual_tokens: int
) -> tuple[int, int]:
    """What the API does for you when an image is over its tier's limits.

    There are TWO ceilings, not one: a longest-edge limit and a visual-token
    limit. An image can clear the edge limit and still be over the token cap,
    so both are applied. Verified against the docs' own worked example:
    1920x1080 on the standard tier (1568 long edge, 1568 token cap) lands at
    1560 visual tokens, not the 1792 you get from the edge limit alone.
    """
    longest = max(width, height)
    if longest > max_long_edge:
        scale = max_long_edge / longest
        width, height = max(1, round(width * scale)), max(1, round(height * scale))
    if visual_tokens(width, height) > max_visual_tokens:
        width, height = resize_for_budget(width, height, max_visual_tokens)
    return width, height


def resize_for_budget(width: int, height: int, token_budget: int) -> tuple[int, int]:
    """Largest same-aspect size that fits a token budget. The ten-minute fix
    the episode mentions, for a pipeline that is over budget."""
    if visual_tokens(width, height) <= token_budget:
        return width, height
    scale = math.sqrt(token_budget * PATCH * PATCH / (width * height))
    w, h = max(PATCH, int(width * scale)), max(PATCH, int(height * scale))
    while visual_tokens(w, h) > token_budget and w > PATCH and h > PATCH:
        w, h = int(w * 0.98), int(h * 0.98)
    return w, h


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("width", type=int, nargs="?")
    ap.add_argument("height", type=int, nargs="?")
    ap.add_argument("--file", help="read the dimensions from a real image")
    ap.add_argument("--long-edge", type=int, default=None,
                    help="your model tier's max long edge, to see the downscale first")
    ap.add_argument("--token-cap", type=int, default=None,
                    help="your model tier's max visual tokens (pairs with --long-edge)")
    ap.add_argument("--budget", type=int, default=None,
                    help="token budget per image, to get a resize target back")
    args = ap.parse_args()

    if args.file:
        from PIL import Image
        with Image.open(args.file) as im:
            w, h = im.size
    elif args.width and args.height:
        w, h = args.width, args.height
    else:
        ap.error("give width and height, or --file")

    print(f"source          {w} x {h}")
    if args.long_edge:
        cap = args.token_cap if args.token_cap else 10 ** 9
        w2, h2 = downscale_for_tier(w, h, args.long_edge, cap)
        if (w2, h2) != (w, h):
            print(f"downscaled to   {w2} x {h2}  (tier caps: long edge "
                  f"{args.long_edge}, tokens {args.token_cap or 'n/a'})")
        w, h = w2, h2

    across, down = math.ceil(w / PATCH), math.ceil(h / PATCH)
    print(f"patch grid      {across} x {down}  ({PATCH}px patches)")
    print(f"visual tokens   {across * down}")

    if args.budget:
        tw, th = resize_for_budget(w, h, args.budget)
        print(f"budget {args.budget:<9} resize to {tw} x {th} -> {visual_tokens(tw, th)} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
