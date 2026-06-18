"""
Configuration settings for the AI Educational Content Creator.
"""
from pydantic import BaseModel, Field
from typing import Optional, Tuple
import os
from pathlib import Path


class VisualizationSettings(BaseModel):
    """Settings for visualization rendering."""
    manim_quality: str = Field(default="medium_quality", description="Manim render quality")
    matplotlib_dpi: int = Field(default=100, description="Matplotlib DPI")
    plotly_width: int = Field(default=800, description="Plotly plot width")
    plotly_height: int = Field(default=600, description="Plotly plot height")
    default_fps: int = Field(default=30, description="Default frames per second")


class AudioSettings(BaseModel):
    """Settings for audio recording and processing."""
    sample_rate: int = Field(default=44100, description="Audio sample rate in Hz")
    channels: int = Field(default=1, description="Number of audio channels (1=mono, 2=stereo)")
    noise_reduction: bool = Field(default=True, description="Enable noise reduction")
    normalize: bool = Field(default=True, description="Enable audio normalization")
    auto_ducking: bool = Field(default=True, description="Enable automatic music ducking")
    ducking_amount: int = Field(default=-10, description="Music volume reduction in dB during speech")


class VideoSettings(BaseModel):
    """Settings for video rendering and export."""
    resolution: Tuple[int, int] = Field(default=(1920, 1080), description="Video resolution (width, height)")
    fps: int = Field(default=30, description="Frames per second")
    bitrate: str = Field(default="5000k", description="Video bitrate")
    codec: str = Field(default="libx264", description="Video codec")
    audio_codec: str = Field(default="aac", description="Audio codec")
    quality_preset: str = Field(default="medium", description="Encoding quality preset")


class AISettings(BaseModel):
    """Settings for AI integration."""
    provider: str = Field(default="gemini", description="AI provider (gemini, openai, anthropic)")
    model: str = Field(default="gemini-1.5-flash-latest", description="AI model name")
    temperature: float = Field(default=0.7, description="AI temperature (0.0-1.0)")
    max_tokens: int = Field(default=8000, description="Maximum tokens per request")
    timeout: int = Field(default=60, description="Request timeout in seconds")


class PathSettings(BaseModel):
    """Settings for file paths."""
    projects_dir: Path = Field(default=Path("data/projects"), description="Projects directory")
    assets_dir: Path = Field(default=Path("assets"), description="Assets directory")
    cache_dir: Path = Field(default=Path(".cache"), description="Cache directory")
    temp_dir: Path = Field(default=Path("temp"), description="Temporary files directory")
    
    def ensure_directories(self):
        """Create directories if they don't exist."""
        for path in [self.projects_dir, self.assets_dir, self.cache_dir, self.temp_dir]:
            path.mkdir(parents=True, exist_ok=True)


class AppSettings(BaseModel):
    """Main application settings."""
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    cache_enabled: bool = Field(default=True, description="Enable caching")
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    
    visualization: VisualizationSettings = Field(default_factory=VisualizationSettings)
    audio: AudioSettings = Field(default_factory=AudioSettings)
    video: VideoSettings = Field(default_factory=VideoSettings)
    ai: AISettings = Field(default_factory=AISettings)
    paths: PathSettings = Field(default_factory=PathSettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure all directories exist
        self.paths.ensure_directories()


# Global settings instance
_settings: Optional[AppSettings] = None


def get_settings() -> AppSettings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings


def reload_settings():
    """Reload settings from environment."""
    global _settings
    _settings = AppSettings()
    return _settings

# Made with Bob
