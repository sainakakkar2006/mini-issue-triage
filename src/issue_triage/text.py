from __future__ import annotations

import re


STOP_WORDS = {
    "a",
    "after",
    "and",
    "for",
    "in",
    "is",
    "of",
    "on",
    "the",
    "to",
    "users",
    "with",
}


def tokenize(text: str) -> set[str]:
    words = {word.lower() for word in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text)}
    return {word for word in words if word not in STOP_WORDS}


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)

