#!/usr/bin/env python3
"""
OpenClaw skill: Rick Sanchez Voice Messages

This skill converts OpenClaw's text responses into Rick Sanchez voice messages
for Telegram delivery.

Usage from OpenClaw:
    When a user requests a voice message, use this skill to generate audio
    and send it as a Telegram voice note.
"""

import os
import sys
import tempfile


def generate_voice_message(text: str, output_path: str = None) -> str:
    """Generate a Rick Sanchez voice message from text.

    Args:
        text: The text to convert to speech.
        output_path: Where to save the OGG file. If None, uses a temp file.

    Returns:
        Path to the generated OGG Opus audio file.
    """
    from rick_voice import RickVoice

    rick = RickVoice()

    if output_path is None:
        output_path = os.path.join(tempfile.gettempdir(), "rick_voice_msg.ogg")

    ogg_bytes = rick.to_ogg(text)

    with open(output_path, "wb") as f:
        f.write(ogg_bytes)

    return output_path


def generate_voice_bytes(text: str, format: str = "mp3") -> bytes:
    """Generate Rick Sanchez voice audio as bytes.

    Args:
        text: The text to convert to speech.
        format: Audio format — "mp3", "wav", or "ogg".

    Returns:
        Audio bytes.
    """
    from rick_voice import RickVoice

    rick = RickVoice()

    if format == "ogg":
        return rick.to_ogg(text)
    return rick.synthesize(text)


if __name__ == "__main__":
    # CLI usage for testing
    text = " ".join(sys.argv[1:]) or "Wubba lubba dub dub, Morty!"
    path = generate_voice_message(text)
    print(f"Generated: {path}")
