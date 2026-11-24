#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

Writes one satirical sentence to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR, or /output when that is unset).
Deterministic, stdlib only, no network, no reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 320

LINE = (
    "The same lawmakers drafting a 900-page bill to govern AI, crypto, "
    "and the entire internet still ask an intern how to save the draft "
    "as a PDF."
)


def validate(line: str) -> None:
    """Enforce the competition rules for the one-liner."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    # Exactly one sentence: a single terminal period, no other
    # sentence-ending punctuation anywhere in the line.
    body = line[:-1] if line.endswith(".") else line
    if any(ch in body for ch in ".!?"):
        raise ValueError("line must be exactly one sentence")
    if not line.endswith("."):
        raise ValueError("line must end with a period")


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("written entry.txt does not match the line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
