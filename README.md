# 🧪 rick-voice [![PyPI version](https://badge.fury.io/py/rick-voice.svg)](https://badge.fury.io/py/rick-voice)
**Give any bot the voice of Rick Sanchez.**

Turn text into Rick Sanchez speech with one line of Python. Works with OpenClaw, Telegram bots, Discord bots, or anything else.

```python
from rick_voice import RickVoice

rick = RickVoice()
rick.play("I turned myself into a pickle, Morty!")
```

---

## Features

- 🎙️ **Rick Sanchez TTS** — actual Rick voice, not just pitch shifting
- 🔌 **Pluggable providers** — Fish Audio (recommended), ElevenLabs, local (coming soon)
- 📱 **Telegram ready** — generates OGG Opus voice messages out of the box
- 🐾 **OpenClaw skill** — drop-in voice for your OpenClaw assistant
- ⚡ **Streaming** — real-time audio playback
- 🐍 **Simple API** — `synthesize()`, `play()`, `to_ogg()`, done

## Quick Start

### 1. Install

```bash
# With Fish Audio (recommended — Rick voice built in)
pip install rick-voice[fish]

# Or with ElevenLabs
pip install rick-voice[elevenlabs]

# Or both
pip install rick-voice[all]
```

### 2. Get an API key

**Fish Audio** (recommended):
1. Sign up at [fish.audio](https://fish.audio)
2. Get your API key at [fish.audio/account/api](https://fish.audio/account/api)
3. Add some credits (pay-as-you-go, very cheap)

```bash
export FISH_API_KEY="your-key-here"
```

**ElevenLabs** (alternative):
1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Get your API key from settings
3. Find a raspy/sarcastic voice in the [Voice Library](https://elevenlabs.io/voice-library) and copy its ID

```bash
export ELEVENLABS_API_KEY="your-key-here"
export RICK_VOICE_ID="your-voice-id"
export RICK_VOICE_PROVIDER="elevenlabs"
```

### 3. Use it

```bash
# CLI
rick-voice "Wubba lubba dub dub!"

# Interactive mode
rick-voice --interactive

# Save to file
rick-voice --save rick.mp3 "I'm pickle Rick!"

# Save as Telegram voice note
rick-voice --save-ogg rick.ogg "Nobody exists on purpose."
```

## Python API

```python
from rick_voice import RickVoice

rick = RickVoice()

# Play through speakers
rick.play("The universe is basically an animal.")

# Get raw audio bytes (MP3)
audio = rick.synthesize("Science, Morty!")
with open("rick.mp3", "wb") as f:
    f.write(audio)

# Get OGG Opus for Telegram voice messages
ogg = rick.to_ogg("Wubba lubba dub dub!")

# Use a specific provider
rick = RickVoice(provider="elevenlabs")

# Or configure everything
from rick_voice import RickVoiceConfig

config = RickVoiceConfig(
    provider="fish",
    fish_api_key="your-key",
    rickify_enabled=True,  # add stutters and filler words
)
rick = RickVoice(config=config)
```

## OpenClaw Integration

Drop the `openclaw-skill/` folder into your OpenClaw skills directory:

```bash
cp -r openclaw-skill/ ~/.openclaw/skills/rick-voice/
```

Then set your API key and OpenClaw will use Rick's voice for voice messages.

See [openclaw-skill/SKILL.md](openclaw-skill/SKILL.md) for full setup.

## Telegram Bot Example

A complete standalone Telegram bot that replies with Rick's voice:

```bash
export FISH_API_KEY="your-key"
export TELEGRAM_BOT_TOKEN="your-bot-token"
pip install rick-voice[fish] python-telegram-bot
python examples/telegram_bot.py
```

Send any text message → get a Rick Sanchez voice note back.

## Providers

| Provider | Quality | Setup | Cost | Rick Voice? |
|----------|---------|-------|------|-------------|
| **Fish Audio** | ⭐⭐⭐⭐ | Easy | Pay-as-you-go (~$0.01/msg) | ✅ Built in |
| **ElevenLabs** | ⭐⭐⭐⭐⭐ | Medium | Free tier + paid | ❌ Find similar voice |
| **Local** | TBD | Hard | Free | 🔜 Coming soon |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FISH_API_KEY` | Fish Audio API key | For Fish provider |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | For ElevenLabs provider |
| `RICK_VOICE_ID` | ElevenLabs voice ID | For ElevenLabs provider |
| `RICK_VOICE_PROVIDER` | Provider name ("fish" or "elevenlabs") | No (default: "fish") |

## Roadmap

- [x] Fish Audio provider
- [x] ElevenLabs provider
- [x] CLI tool
- [x] OpenClaw skill
- [x] Telegram voice message support (OGG Opus)
- [ ] Local provider (Piper TTS + RVC / Coqui XTTS)
- [ ] Discord bot example
- [ ] Home Assistant integration
- [ ] More characters (Morty, Mr. Meeseeks, etc.)

## License

MIT — do whatever you want with it.

---

*"To live is to risk it all. Otherwise you're just an inert chunk of randomly assembled molecules drifting wherever the universe blows you."* — Rick Sanchez
