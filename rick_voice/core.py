"""Core RickVoice class — the main API for rick-voice."""

from __future__ import annotations

from typing import Optional

from rick_voice.config import RickVoiceConfig
from rick_voice.providers import TTSProvider
from rick_voice.rickifier import rickify


class RickVoice:
    """Rick Sanchez text-to-speech.

    Usage:
        from rick_voice import RickVoice

        rick = RickVoice()  # uses Fish Audio by default
        rick.play("I'm pickle Rick!")

        # Get raw audio bytes (for Telegram, Discord, etc.)
        audio = rick.synthesize("Wubba lubba dub dub!")

        # With ElevenLabs
        rick = RickVoice(provider="elevenlabs")

    Environment variables:
        RICK_VOICE_PROVIDER  - "fish" or "elevenlabs" (default: "fish")
        FISH_API_KEY         - Fish Audio API key
        ELEVENLABS_API_KEY   - ElevenLabs API key
        RICK_VOICE_ID        - ElevenLabs voice ID
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        config: Optional[RickVoiceConfig] = None,
        **kwargs,
    ):
        """Initialize RickVoice.

        Args:
            provider: TTS provider ("fish", "elevenlabs", or "local").
                      Overrides config.provider if set.
            config: Full config object. If None, creates from env vars.
            **kwargs: Passed to RickVoiceConfig if config is None.
        """
        if config is None:
            config = RickVoiceConfig(
                provider=provider or "fish",
                **kwargs,
            )
        elif provider is not None:
            config.provider = provider

        self.config = config
        self._provider: Optional[TTSProvider] = None

    @property
    def provider(self) -> TTSProvider:
        """Lazy-load the TTS provider."""
        if self._provider is None:
            self._provider = self._create_provider()
        return self._provider

    def _create_provider(self) -> TTSProvider:
        """Create the appropriate TTS provider based on config."""
        name = self.config.provider.lower()

        if name == "fish":
            from rick_voice.providers.fish_audio import FishAudioProvider
            return FishAudioProvider(self.config)

        elif name == "elevenlabs":
            from rick_voice.providers.elevenlabs import ElevenLabsProvider
            return ElevenLabsProvider(self.config)

        elif name == "local":
            raise NotImplementedError(
                "Local provider coming soon! "
                "Use 'fish' or 'elevenlabs' for now."
            )

        else:
            raise ValueError(
                f"Unknown provider: {name!r}. "
                f"Choose from: 'fish', 'elevenlabs'"
            )

    def _prepare_text(self, text: str) -> str:
        """Apply rickifier if enabled."""
        if self.config.rickify_enabled:
            return rickify(text, self.config.rickify_intensity)
        return text

    def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes in Rick's voice.

        Args:
            text: Text to speak.

        Returns:
            Audio bytes (MP3 by default).
        """
        prepared = self._prepare_text(text)
        return self.provider.synthesize(prepared)

    def play(self, text: str) -> None:
        """Speak text through speakers in Rick's voice.

        Args:
            text: Text to speak.
        """
        prepared = self._prepare_text(text)
        self.provider.play(prepared)

    def stream(self, text: str):
        """Stream audio chunks in Rick's voice.

        Args:
            text: Text to speak.

        Returns:
            Iterator of audio chunks.
        """
        prepared = self._prepare_text(text)
        return self.provider.stream(prepared)

    def to_ogg(self, text: str) -> bytes:
        """Generate OGG Opus audio — ideal for Telegram voice messages.

        Args:
            text: Text to speak.

        Returns:
            OGG Opus audio bytes.
        """
        import subprocess
        import tempfile
        import os

        mp3_bytes = self.synthesize(text)

        tmp_in = os.path.join(tempfile.gettempdir(), "rick_voice_in.mp3")
        tmp_out = os.path.join(tempfile.gettempdir(), "rick_voice_out.ogg")

        with open(tmp_in, "wb") as f:
            f.write(mp3_bytes)

        subprocess.run(
            [
                "ffmpeg", "-y", "-i", tmp_in,
                "-c:a", "libopus", "-b:a", "64k",
                tmp_out,
            ],
            capture_output=True,
            check=True,
        )

        with open(tmp_out, "rb") as f:
            ogg_bytes = f.read()

        os.unlink(tmp_in)
        os.unlink(tmp_out)

        return ogg_bytes
