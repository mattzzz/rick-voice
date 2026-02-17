"""Configuration for rick-voice."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RickVoiceConfig:
    """Configuration for Rick Voice TTS.

    Provider can be "fish", "elevenlabs", or "local" (coming soon).

    API keys are read from the config or fall back to environment variables:
      - FISH_API_KEY
      - ELEVENLABS_API_KEY
      - RICK_VOICE_ID  (for ElevenLabs)
    """

    # Which TTS provider to use: "fish", "elevenlabs", "local"
    provider: str = "fish"

    # Fish Audio settings
    fish_api_key: Optional[str] = None
    fish_voice_id: str = "d2e75a3e3fd6419893057c02a375a113"  # Rick Sanchez model

    # ElevenLabs settings
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None  # User must find/set this
    elevenlabs_model_id: str = "eleven_v3"
    elevenlabs_stability: float = 0.3
    elevenlabs_similarity_boost: float = 0.85
    elevenlabs_style: float = 0.7

    # Audio output settings
    output_format: str = "mp3"  # "mp3", "wav", "pcm", "ogg"

    # Rickifier settings
    rickify_enabled: bool = False  # Off by default — voice model handles it
    rickify_intensity: float = 0.3

    def __post_init__(self):
        # Fall back to environment variables for API keys
        if self.fish_api_key is None:
            self.fish_api_key = os.environ.get("FISH_API_KEY", "")
        if self.elevenlabs_api_key is None:
            self.elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        if self.elevenlabs_voice_id is None:
            self.elevenlabs_voice_id = os.environ.get("RICK_VOICE_ID", "")

    @classmethod
    def from_env(cls, provider: Optional[str] = None) -> "RickVoiceConfig":
        """Create config from environment variables.

        Set RICK_VOICE_PROVIDER to "fish" or "elevenlabs".
        """
        return cls(
            provider=provider or os.environ.get("RICK_VOICE_PROVIDER", "fish"),
        )
