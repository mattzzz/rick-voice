#!/usr/bin/env python3
"""
Example: Standalone Telegram bot that responds with Rick's voice.

Requirements:
    pip install rick-voice[fish] python-telegram-bot

Usage:
    export FISH_API_KEY="your-fish-audio-key"
    export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
    python telegram_bot.py
"""

import os
import tempfile

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from rick_voice import RickVoice

# Initialize Rick
rick = RickVoice()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm Rick Sanchez, b*tch! Send me any text and "
        "I'll say it back to you in my voice. Let's go!"
    )


async def voice_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Convert user's text message to a Rick Sanchez voice note."""
    text = update.message.text

    # Generate OGG audio for Telegram voice message
    ogg_bytes = rick.to_ogg(text)

    # Send as voice message
    tmp = os.path.join(tempfile.gettempdir(), "rick_reply.ogg")
    with open(tmp, "wb") as f:
        f.write(ogg_bytes)

    with open(tmp, "rb") as f:
        await update.message.reply_voice(voice=f)


def main():
    if not BOT_TOKEN:
        print("Set TELEGRAM_BOT_TOKEN environment variable")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, voice_reply))

    print("Rick bot is running... Send a message on Telegram!")
    app.run_polling()


if __name__ == "__main__":
    main()
