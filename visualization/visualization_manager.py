"""
Unified visualization manager for all renderer types.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import time
from .base_renderer import (
    BaseRenderer, RenderResult, RenderConfig,
    VisualizationType, RenderQuality
)
from .manim_renderer import ManimRenderer
from .matplotlib_renderer import MatplotlibRenderer
from .plotly_renderer import PlotlyRenderer


class VisualizationManager:
    """Manage all visualization renderers with a unified interface."""
    
    def __init__(self, config: Optional[RenderConfig] = None):
        """
        Initialize visualization manager.
        
        Args:
            config: Default render configuration
        """
        self.config = config or RenderConfig()
        self.renderers: Dict[str, BaseRenderer] = {}
        self._initialize_renderers()
    
    def _initialize_renderers(self):
        """Initialize all available renderers."""
        self.renderers = {
            VisualizationType.MANIM.value: ManimRenderer(self.config),
            VisualizationType.MATPLOTLIB.value: MatplotlibRenderer(self.config),
            VisualizationType.PLOTLY.value: PlotlyRenderer(self.config)
        }
    
    def render_scene(
        self,
        scene_data: Dict[str, Any],
        output_path: Optional[Path] = None,
        quality: Optional[RenderQuality] = None
    ) -> RenderResult:
        """
        Render a scene using the appropriate renderer.
        
        Args:
            scene_data: Scene configuration and content
            output_path: Optional output path (auto-generated if not provided)
            quality: Optional quality override
            
        Returns:
            RenderResult with rendering outcome
        """
        # Determine visualization type
        viz_type = scene_data.get("visualization_type", "matplotlib").lower()
        
        if viz_type not in self.renderers:
            return RenderResult(
                success=False,
                error=f"Unknown visualization type: {viz_type}"
            )
        
        # Get renderer
        renderer = self.renderers[viz_type]
        
        # Override quality if specified
        if quality:
            original_quality = renderer.config.quality
            renderer.config.quality = quality
        
        # Generate output path if not provided
        if output_path is None:
            scene_id = scene_data.get("id", "scene")
            output_path = Path(f"temp/renders/scene_{scene_id}_{int(time.time())}.mp4")
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Render
        result = renderer.render(scene_data, output_path)
        
        # Restore quality
        if quality:
            renderer.config.quality = original_quality
        
        return result
    
    def preview_scene(self, scene_data: Dict[str, Any]) -> RenderResult:
        """
        Generate quick preview of a scene.
        
        Args:
            scene_data: Scene configuration
            
        Returns:
            RenderResult with preview file
        """
        viz_type = scene_data.get("visualization_type", "matplotlib").lower()
        
        if viz_type not in self.renderers:
            return RenderResult(
                success=False,
                error=f"Unknown visualization type: {viz_type}"
            )
        
        renderer = self.renderers[viz_type]
        return renderer.preview(scene_data)
    
    def validate_scene(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate scene data for its renderer.
        
        Args:
            scene_data: Scene configuration
            
        Returns:
            Dict with validation results
        """
        viz_type = scene_data.get("visualization_type", "matplotlib").lower()
        
        if viz_type not in self.renderers:
            return {
                "valid": False,
                "errors": [f"Unknown visualization type: {viz_type}"],
                "warnings": []
            }
        
        renderer = self.renderers[viz_type]
        return renderer.validate_scene(scene_data)
    
    def render_all_scenes(
        self,
        scenes: List[Dict[str, Any]],
        output_dir: Path,
        quality: Optional[RenderQuality] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, RenderResult]:
        """
        Render multiple scenes.
        
        Args:
            scenes: List of scene configurations
            output_dir: Directory for output files
            quality: Optional quality override
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict mapping scene IDs to RenderResults
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        results = {}
        
        for i, scene in enumerate(scenes):
            scene_id = scene.get("id", i + 1)
            output_path = output_dir / f"scene_{scene_id}.mp4"
            
            # Render scene
            result = self.render_scene(scene, output_path, quality)
            results[str(scene_id)] = result
            
            # Progress callback
            if progress_callback:
                progress_callback(i + 1, len(scenes), result)
        
        return results
    
    def get_renderer(self, viz_type: str) -> Optional[BaseRenderer]:
        """
        Get specific renderer by type.
        
        Args:
            viz_type: Visualization type
            
        Returns:
            BaseRenderer instance or None
        """
        return self.renderers.get(viz_type.lower())
    
    def get_supported_types(self) -> List[str]:
        """Get list of supported visualization types."""
        return list(self.renderers.keys())
    
    def get_renderer_features(self, viz_type: str) -> List[str]:
        """
        Get supported features for a renderer.
        
        Args:
            viz_type: Visualization type
            
        Returns:
            List of supported features
        """
        renderer = self.get_renderer(viz_type)
        if renderer:
            return renderer.get_supported_features()
        return []
    
    def estimate_total_render_time(self, scenes: List[Dict[str, Any]]) -> float:
        """
        Estimate total rendering time for all scenes.
        
        Args:
            scenes: List of scene configurations
            
        Returns:
            Estimated time in seconds
        """
        total_time = 0.0
        
        for scene in scenes:
            viz_type = scene.get("visualization_type", "matplotlib").lower()
            renderer = self.get_renderer(viz_type)
            
            if renderer:
                total_time += renderer.estimate_render_time(scene)
        
        return total_time
    
    def cleanup_all(self):
        """Clean up temporary files from all renderers."""
        for renderer in self.renderers.values():
            renderer.cleanup_temp_files()
    
    def set_quality(self, quality: RenderQuality):
        """
        Set quality for all renderers.
        
        Args:
            quality: Quality preset to use
        """
        self.config.quality = quality
        for renderer in self.renderers.values():
            renderer.config.quality = quality
    
    def get_renderer_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all renderers.
        
        Returns:
            Dict with renderer information
        """
        info = {}
        
        for viz_type, renderer in self.renderers.items():
            info[viz_type] = {
                "type": viz_type,
                "features": renderer.get_supported_features(),
                "config": {
                    "quality": renderer.config.quality.value,
                    "fps": renderer.config.fps,
                    "resolution": f"{renderer.config.width}x{renderer.config.height}"
                }
            }
        
        return info


# Convenience function for quick rendering
def render_scene(
    scene_data: Dict[str, Any],
    output_path: Optional[Path] = None,
    quality: str = "medium"
) -> RenderResult:
    """
    Quick function to render a single scene.
    
    Args:
        scene_data: Scene configuration
        output_path: Optional output path
        quality: Quality preset ('low', 'medium', 'high', 'ultra')
        
    Returns:
        RenderResult
    """
    quality_enum = RenderQuality[quality.upper()]
    config = RenderConfig.from_quality(quality_enum)
    manager = VisualizationManager(config)
    
    return manager.render_scene(scene_data, output_path)


# Made with Bob