"""ElevenLabs TTS provider."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rick_voice.providers import TTSProvider

if TYPE_CHECKING:
    from rick_voice.config import RickVoiceConfig


class ElevenLabsProvider(TTSProvider):
    """TTS provider using ElevenLabs API.

    Note: ElevenLabs blocks direct "Rick Sanchez" voice clones.
    Users need to find a suitable raspy/sarcastic voice in the
    Voice Library and set the voice ID.

    Requires: pip install elevenlabs
    """

    def __init__(self, config: RickVoiceConfig):
        super().__init__(config)

        try:
            from elevenlabs.client import ElevenLabs
        except ImportError:
            raise ImportError(
                "ElevenLabs SDK not installed. Run: pip install elevenlabs"
            )

        if not config.elevenlabs_api_key:
            raise ValueError(
                "ElevenLabs API key not set. "
                "Set ELEVENLABS_API_KEY env var or pass elevenlabs_api_key in config.\n"
                "Get a key at: https://elevenlabs.io/app/settings/api-keys"
            )

        if not config.elevenlabs_voice_id:
            raise ValueError(
                "ElevenLabs voice ID not set. "
                "Set RICK_VOICE_ID env var or pass elevenlabs_voice_id in config.\n"
                "Browse voices at: https://elevenlabs.io/voice-library"
            )

        self._client = ElevenLabs(api_key=config.elevenlabs_api_key)

    def _voice_settings(self) -> dict:
        return {
            "stability": self.config.elevenlabs_stability,
            "similarity_boost": self.config.elevenlabs_similarity_boost,
            "style": self.config.elevenlabs_style,
        }

    def _output_format(self) -> str:
        """Map generic format names to ElevenLabs format strings."""
        fmt = self.config.output_format
        mapping = {
            "mp3": "mp3_44100_128",
            "wav": "pcm_44100",
            "pcm": "pcm_22050",
        }
        return mapping.get(fmt, fmt)

    def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes via ElevenLabs."""
        audio = self._client.text_to_speech.convert(
            text=text,
            voice_id=self.config.elevenlabs_voice_id,
            model_id=self.config.elevenlabs_model_id,
            output_format=self._output_format(),
            voice_settings=self._voice_settings(),
        )

        # Collect generator chunks
        chunks = []
        for chunk in audio:
            if isinstance(chunk, bytes):
                chunks.append(chunk)
        return b"".join(chunks)

    def stream(self, text: str):
        """Stream audio chunks via ElevenLabs."""
        return self._client.text_to_speech.stream(
            text=text,
            voice_id=self.config.elevenlabs_voice_id,
            model_id=self.config.elevenlabs_model_id,
            voice_settings=self._voice_settings(),
        )

    def play(self, text: str) -> None:
        """Stream and play audio via ElevenLabs' built-in streamer."""
        try:
            from elevenlabs import stream as el_stream

            audio_stream = self.stream(text)
            el_stream(audio_stream)
        except ImportError:
            super().play(text)
