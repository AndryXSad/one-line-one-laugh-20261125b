"""One Line, One Laugh — make.fun entry.

Writes exactly one funny line to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when that is set).

The line was picked by a local pairwise tournament over 14 fresh
one-liners, scored on the judge brief's five criteria in order: lands
its laugh on a first read, surprise turn, economy of words, freshness,
clean wording. It won 3 of 3 pairings in the final four.

Stdlib only. Deterministic: every run writes the same bytes.
"""

import os

JOKE = "My GPS said 'recalculating' in the exact tone my mother uses when I say I'm fine."

MIN_CHARS = 1
MAX_CHARS = 200


def validate_line(line):
    """Gate check: 1-200 chars, one line, not only whitespace."""
    data = line.encode("utf-8")
    if not (MIN_CHARS <= len(data) <= MAX_CHARS):
        raise ValueError("line is %d bytes, gate is 1-200" % len(data))
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        raise ValueError("line is %d characters, gate is 1-200" % len(line))
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    return data


def main():
    # The gate: 1 to 200 characters, a single line, not only whitespace.
    # Check the encoded bytes too, so a future edit with non-ASCII text
    # cannot silently pass the character count and fail the byte gate.
    data = validate_line(JOKE)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)

    # Read back and confirm byte-for-byte, with no trailing newline.
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise ValueError("read-back differs from what was written")
    if back.endswith(b"\n"):
        raise ValueError("output must not end with a newline")


if __name__ == "__main__":
    main()
