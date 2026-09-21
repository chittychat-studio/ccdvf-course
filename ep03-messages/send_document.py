"""EP 03, move three (second half): sending a PDF.

A PDF is a `document` block, not an `image` block. The source structure is the
same three options as an image, so nothing else about the request changes.

  base64  - the bytes inline. Simple. Travels with every request.
  url     - a link the API fetches.
  file    - a Files API file_id. Upload once, reference many times.

A document block has no required `name` field. `title` and `context` are both
optional. Docs: https://platform.claude.com/docs/en/build-with-claude/pdf-support

Run:  python send_document.py contract.pdf "List every payment obligation."
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-5"


def block_from_base64(path: Path) -> dict:
    return {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": base64.standard_b64encode(path.read_bytes()).decode("ascii"),
        },
        "title": path.name,
    }


def block_from_url(url: str) -> dict:
    return {"type": "document", "source": {"type": "url", "url": url}}


def block_from_file_id(file_id: str) -> dict:
    """Upload once with the Files API, then reference it by id in every request.
    Right whenever the same document is sent more than once."""
    return {"type": "document", "source": {"type": "file", "file_id": file_id}}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    path, question = Path(sys.argv[1]), sys.argv[2]

    # The prompting rules from module 2 still apply to a document. A bare
    # "summarise this" gets you a shallow answer for exactly the same reason a
    # bare text prompt does. Name the shape you want back.
    client = Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    block_from_base64(path),
                    {
                        "type": "text",
                        "text": (
                            f"{question}\n\n"
                            "Answer as a numbered list. Quote the clause each item "
                            "comes from. If the document does not say, write NOT STATED "
                            "rather than inferring it."
                        ),
                    },
                ],
            }
        ],
    )
    print(response.content[0].text)
    print("\ninput tokens:", response.usage.input_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
