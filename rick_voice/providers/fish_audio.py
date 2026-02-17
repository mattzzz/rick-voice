"""Fish Audio TTS provider."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rick_voice.providers import TTSProvider

if TYPE_CHECKING:
    from rick_voice.config import RickVoiceConfig


class FishAudioProvider(TTSProvider):
    """TTS provider using Fish Audio API.

    Fish Audio has a community Rick Sanchez voice model available
    out of the box — no voice cloning or setup needed.

    Requires: pip install "fish-audio-sdk[utils]"
    """

    def __init__(self, config: RickVoiceConfig):
        super().__init__(config)

        try:
            from fishaudio import FishAudio
        except ImportError:
            raise ImportError(
                'Fish Audio SDK not installed. Run: pip install "fish-audio-sdk[utils]"'
            )

        if not config.fish_api_key:
            raise ValueError(
                "Fish Audio API key not set. "
                "Set FISH_API_KEY env var or pass fish_api_key in config.\n"
                "Get a key at: https://fish.audio/account/api"
            )

        self._client = FishAudio(api_key=config.fish_api_key)

    def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes via Fish Audio."""
        from fishaudio.types import TTSConfig

        config = TTSConfig(
            reference_id=self.config.fish_voice_id,
            format=self.config.output_format,
        )

        audio = self._client.tts.convert(text=text, config=config)

        # Handle both bytes and generator responses
        if isinstance(audio, bytes):
            return audio

        chunks = []
        for chunk in audio:
            if isinstance(chunk, bytes):
                chunks.append(chunk)
        return b"".join(chunks)

    def stream(self, text: str):
        """Stream audio chunks via Fish Audio."""
        from fishaudio.types import TTSConfig

        config = TTSConfig(
            reference_id=self.config.fish_voice_id,
            latency="balanced",
        )

        return self._client.tts.stream(text=text, config=config)

    def play(self, text: str) -> None:
        """Stream and play audio via Fish Audio's built-in player."""
        try:
            from fishaudio.utils import play

            audio = self.synthesize(text)
            play(audio)
        except ImportError:
            # Fall back to base implementation
            super().play(text)
