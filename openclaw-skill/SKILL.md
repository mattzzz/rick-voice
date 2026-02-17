# Rick Voice — OpenClaw Skill

This skill gives OpenClaw the voice of Rick Sanchez when sending Telegram voice messages.

## Setup

1. Install the rick-voice package:
   ```
   pip install rick-voice[fish]
   ```

2. Set your Fish Audio API key:
   ```
   export FISH_API_KEY="your-key-here"
   ```
   Get one at: https://fish.audio/account/api

3. Copy this `openclaw-skill/` folder into your OpenClaw skills directory.

## How It Works

When OpenClaw needs to send a voice message, this skill converts the text response
into audio using Rick Sanchez's voice via Fish Audio's TTS API, then sends it as
a Telegram voice note.

## Usage

Tell OpenClaw: "Send me a voice message saying..."
Or configure OpenClaw to always respond with voice.

## Switching Providers

To use ElevenLabs instead of Fish Audio:
```
export RICK_VOICE_PROVIDER="elevenlabs"
export ELEVENLABS_API_KEY="your-key"
export RICK_VOICE_ID="your-voice-id"
```

## Python API

```python
from rick_voice import RickVoice

rick = RickVoice()

# Get audio bytes to send via Telegram
audio_bytes = rick.synthesize("I'm pickle Rick!")

# Get OGG Opus for Telegram voice messages
ogg_bytes = rick.to_ogg("Wubba lubba dub dub!")
```
