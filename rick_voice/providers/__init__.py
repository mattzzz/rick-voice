"""Abstract base class for TTS providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rick_voice.config import RickVoiceConfig


class TTSProvider(ABC):
    """Base class for all TTS providers."""

    def __init__(self, config: RickVoiceConfig):
        self.config = config

    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes.

        Args:
            text: Text to speak.

        Returns:
            Audio bytes (format depends on config.output_format).
        """
        ...

    @abstractmethod
    def stream(self, text: str):
        """Stream audio for real-time playback.

        Args:
            text: Text to speak.

        Returns:
            Iterator/generator of audio chunks.
        """
        ...

    def play(self, text: str) -> None:
        """Synthesize and play audio through speakers.

        Args:
            text: Text to speak.
        """
        # Default implementation — providers can override for streaming playback
        audio = self.synthesize(text)
        self._play_bytes(audio)

    def _play_bytes(self, audio: bytes) -> None:
        """Play raw audio bytes through speakers."""
        import subprocess
        import tempfile
        import os

        ext = self.config.output_format or "mp3"
        tmp = os.path.join(tempfile.gettempdir(), f"rick_voice_out.{ext}")
        with open(tmp, "wb") as f:
            f.write(audio)

        # Try common players
        for player in ["mpv", "ffplay", "afplay", "aplay"]:
            try:
                subprocess.run(
                    [player, "--no-video", tmp] if player == "mpv"
                    else [player, "-nodisp", "-autoexit", tmp] if player == "ffplay"
                    else [player, tmp],
                    capture_output=True,
                    check=True,
                )
                return
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue

        raise RuntimeError(
            "No audio player found. Install mpv, ffmpeg, or use .synthesize() "
            "to get raw bytes instead."
        )
