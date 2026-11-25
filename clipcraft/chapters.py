"""Split a script into chapters, one image and one voice clip per chapter. Author: WR"""

import re

SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")


def split_into_chapters(text: str, max_length: int) -> list[str]:
    """Group whole sentences into chapters no longer than max_length characters.

    A single sentence longer than max_length becomes its own chapter.
    """
    if max_length < 1:
        raise ValueError("max_length must be positive")
    chapters, current = [], ""
    for sentence in SENTENCE_END.split(" ".join(text.split())):
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > max_length:
            chapters.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        chapters.append(current)
    return chapters
