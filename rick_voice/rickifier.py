"""Text rickifier — adds Rick Sanchez speech patterns."""

import random


def rickify(text: str, intensity: float = 0.3) -> str:
    """Inject Rick Sanchez speech mannerisms into text.

    Adds stutters, filler words, and occasional "Morty" suffixes.
    Burps are intentionally excluded since TTS can't render them.

    Args:
        text: Input text to rickify.
        intensity: How aggressively to inject mannerisms (0.0 to 1.0).

    Returns:
        Rickified text string.
    """
    fillers = [
        "y'know,", "listen,", "look,", "I mean,",
        "here's the thing,", "and-and-and,",
    ]

    words = text.split()
    result = []

    for i, word in enumerate(words):
        # Random stutter on longer words
        if random.random() < intensity * 0.1 and len(word) > 3:
            result.append(f"{word[:2]}-{word}")
        else:
            result.append(word)

        # Random filler injection
        if random.random() < intensity * 0.08:
            result.append(random.choice(fillers))

    # Occasional "Morty" suffix
    if random.random() < intensity and not text.rstrip().endswith("Morty"):
        result.append(", Morty.")

    return " ".join(result)
