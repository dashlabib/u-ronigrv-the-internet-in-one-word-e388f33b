#!/usr/bin/env python3
"""The Internet in One Word.

Writes a single word describing the whole internet to /output/entry.txt
and nothing else. Stdlib only, fully deterministic: the same bytes on
every run.

The word: "enshittification" — the process by which every corner of the
internet, once useful and free, is steadily degraded to squeeze out
value: search results full of ads, feeds full of engagement bait, apps
full of dark patterns, everything a little worse than it was last year.
It is funny on its own, true of the internet as a whole rather than any
one site, surprising as a description, and instantly readable.
"""

import hashlib
import os
import sys
import tempfile

WORD = "enshittification"


def validate_word(word):
    """Enforce the sealed gate before anything is written.

    The gate requires /output/entry.txt to be UTF-8 text of 1 to 30
    characters, not only white space; the bounty requires a single word,
    so the word must also hold no whitespace at all and no line breaks.
    Raises ValueError on any violation; returns the word unchanged.
    """
    if not isinstance(word, str):
        raise ValueError("gate: word is not text")
    if not 1 <= len(word) <= 30:
        raise ValueError("gate: word must be 1-30 characters, got %d" % len(word))
    if not word.strip():
        raise ValueError("gate: word must not be only white space")
    if any(ch.isspace() for ch in word):
        raise ValueError("gate: word must be a single word (no whitespace)")
    word.encode("utf-8")  # raises if not encodable as UTF-8
    return word


def entry_bytes():
    """The exact bytes written to /output/entry.txt: the word, no newline."""
    return validate_word(WORD).encode("utf-8")


def write_entry(output_dir):
    """Write the word to <output_dir>/entry.txt, creating the dir if needed."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(entry_bytes())
    return path


def self_test():
    """Prove determinism: two independent runs produce byte-identical files."""
    digests = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_entry(tmp)
            with open(path, "rb") as f:
                data = f.read()
            digests.append(hashlib.sha256(data).hexdigest())
            assert data == entry_bytes(), "self-test: output differs from WORD"
    assert digests[0] == digests[1], "self-test: runs are not deterministic"
    print("self-test PASS")
    print("word: %s" % WORD)
    print("bytes: %d" % len(entry_bytes()))
    print("sha256: %s" % digests[0])
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    path = write_entry(output_dir)
    print("wrote %s (%d bytes)" % (path, len(entry_bytes())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
