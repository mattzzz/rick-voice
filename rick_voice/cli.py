#!/usr/bin/env python3
"""CLI for rick-voice — speak text as Rick Sanchez."""

import argparse
import sys

from rick_voice.config import RickVoiceConfig
from rick_voice.core import RickVoice


DEMO_QUOTES = [
    "I'm sorry, but your opinion means very little to me.",
    "Nobody exists on purpose. Nobody belongs anywhere. We're all going to die.",
    "To live is to risk it all. Otherwise you're just an inert chunk of randomly assembled molecules.",
    "I turned myself into a pickle! I'm Pickle Rick!",
    "Wubba lubba dub dub!",
    "The universe is basically an animal. It grazes on the ordinary.",
]


def main():
    parser = argparse.ArgumentParser(
        prog="rick-voice",
        description="Text-to-speech in Rick Sanchez's voice",
        epilog="Example: rick-voice 'Wubba lubba dub dub!'",
    )
    parser.add_argument("text", nargs="*", help="Text to speak")
    parser.add_argument(
        "-p", "--provider",
        choices=["fish", "elevenlabs"],
        default=None,
        help="TTS provider (default: fish, or RICK_VOICE_PROVIDER env var)",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode — type lines, Rick speaks them",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from stdin",
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        metavar="FILE",
        help="Save audio to file instead of playing (e.g. --save rick.mp3)",
    )
    parser.add_argument(
        "--save-ogg",
        type=str,
        default=None,
        metavar="FILE",
        help="Save as OGG Opus (ideal for Telegram voice messages)",
    )
    parser.add_argument(
        "--rickify",
        action="store_true",
        help="Add stutters and filler words to text",
    )

    args = parser.parse_args()

    # Build config
    config = RickVoiceConfig.from_env(provider=args.provider)
    config.rickify_enabled = args.rickify
    rick = RickVoice(config=config)

    # Save to OGG
    if args.save_ogg:
        text = " ".join(args.text) if args.text else _random_quote()
        print(f"[Rick] {text}")
        print("[...] Generating OGG...", file=sys.stderr)
        ogg = rick.to_ogg(text)
        with open(args.save_ogg, "wb") as f:
            f.write(ogg)
        print(f"[OK] Saved to {args.save_ogg}", file=sys.stderr)
        return

    # Save to file
    if args.save:
        text = " ".join(args.text) if args.text else _random_quote()
        print(f"[Rick] {text}")
        print("[...] Generating audio...", file=sys.stderr)
        audio = rick.synthesize(text)
        with open(args.save, "wb") as f:
            f.write(audio)
        print(f"[OK] Saved to {args.save}", file=sys.stderr)
        return

    # Interactive mode
    if args.interactive:
        print("=== Rick Sanchez TTS ===")
        print(f"Provider: {config.provider}")
        print("Type something and Rick will say it. Ctrl+C to quit.\n")
        try:
            while True:
                text = input("You: ").strip()
                if text:
                    rick.play(text)
                    print()
        except (KeyboardInterrupt, EOFError):
            print("\n[Rick] Peace out, losers!")
        return

    # Stdin mode
    if args.stdin:
        text = sys.stdin.read().strip()
        if text:
            rick.play(text)
        return

    # Positional text
    if args.text:
        rick.play(" ".join(args.text))
        return

    # No input — play a random quote
    quote = _random_quote()
    print(f"[Rick] {quote}")
    rick.play(quote)


def _random_quote() -> str:
    import random
    return random.choice(DEMO_QUOTES)


if __name__ == "__main__":
    main()
