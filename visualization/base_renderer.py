"""
Base classes and interfaces for visualization renderers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class VisualizationType(Enum):
    """Supported visualization types."""
    MANIM = "manim"
    MATPLOTLIB = "matplotlib"
    PLOTLY = "plotly"


class RenderQuality(Enum):
    """Render quality presets."""
    LOW = "low"           # Fast preview, 480p
    MEDIUM = "medium"     # Standard, 720p
    HIGH = "high"         # Production, 1080p
    ULTRA = "ultra"       # 4K, slow


@dataclass
class RenderConfig:
    """Configuration for rendering."""
    quality: RenderQuality = RenderQuality.MEDIUM
    fps: int = 30
    width: int = 1920
    height: int = 1080
    background_color: str = "#000000"
    output_format: str = "mp4"
    
    @classmethod
    def from_quality(cls, quality: RenderQuality) -> 'RenderConfig':
        """Create config from quality preset."""
        configs = {
            RenderQuality.LOW: cls(quality=quality, width=854, height=480, fps=24),
            RenderQuality.MEDIUM: cls(quality=quality, width=1280, height=720, fps=30),
            RenderQuality.HIGH: cls(quality=quality, width=1920, height=1080, fps=30),
            RenderQuality.ULTRA: cls(quality=quality, width=3840, height=2160, fps=60)
        }
        return configs.get(quality, cls())


@dataclass
class RenderResult:
    """Result of a rendering operation."""
    success: bool
    output_path: Optional[Path] = None
    duration: float = 0.0  # seconds
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseRenderer(ABC):
    """Abstract base class for all visualization renderers."""
    
    def __init__(self, config: Optional[RenderConfig] = None):
        """
        Initialize renderer.
        
        Args:
            config: Render configuration (uses default if not provided)
        """
        self.config = config or RenderConfig()
        self.output_dir = Path("temp/renders")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def render(self, scene_data: Dict[str, Any], output_path: Path) -> RenderResult:
        """
        Render a scene to video file.
        
        Args:
            scene_data: Scene configuration and content
            output_path: Path for output video file
            
        Returns:
            RenderResult: Result of rendering operation
        """
        pass
    
    @abstractmethod
    def preview(self, scene_data: Dict[str, Any]) -> RenderResult:
        """
        Generate a quick preview of the scene.
        
        Args:
            scene_data: Scene configuration and content
            
        Returns:
            RenderResult: Result with preview file path
        """
        pass
    
    @abstractmethod
    def validate_scene(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate scene data for this renderer.
        
        Args:
            scene_data: Scene configuration to validate
            
        Returns:
            Dict with validation results
        """
        pass
    
    def get_supported_features(self) -> List[str]:
        """
        Get list of supported features for this renderer.
        
        Returns:
            List of feature names
        """
        return []
    
    def estimate_render_time(self, scene_data: Dict[str, Any]) -> float:
        """
        Estimate rendering time in seconds.
        
        Args:
            scene_data: Scene configuration
            
        Returns:
            Estimated time in seconds
        """
        duration = scene_data.get("duration", 30)
        # Base estimate: 2x real-time for medium quality
        multiplier = {
            RenderQuality.LOW: 1.0,
            RenderQuality.MEDIUM: 2.0,
            RenderQuality.HIGH: 3.0,
            RenderQuality.ULTRA: 5.0
        }.get(self.config.quality, 2.0)
        
        return duration * multiplier
    
    def cleanup_temp_files(self):
        """Clean up temporary files created during rendering."""
        import shutil
        temp_dir = Path("temp/renders")
        if temp_dir.exists():
            for file in temp_dir.glob("*_temp_*"):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error cleaning up {file}: {e}")


class RendererError(Exception):
    """Base exception for renderer errors."""
    pass


class RenderTimeoutError(RendererError):
    """Raised when rendering times out."""
    pass


class InvalidSceneDataError(RendererError):
    """Raised when scene data is invalid."""
    pass


class RenderingFailedError(RendererError):
    """Raised when rendering fails."""
    pass


# Made with Bob