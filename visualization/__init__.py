"""
Visualization module for rendering educational content.

Supports multiple rendering engines:
- Manim: Mathematical animations
- Matplotlib: Graphs and plots
- Plotly: 3D and interactive visualizations
"""

from .base_renderer import (
    BaseRenderer,
    RenderConfig,
    RenderResult,
    RenderQuality,
    VisualizationType,
    RendererError,
    RenderTimeoutError,
    InvalidSceneDataError,
    RenderingFailedError
)

from .manim_renderer import ManimRenderer
from .matplotlib_renderer import MatplotlibRenderer
from .plotly_renderer import PlotlyRenderer
from .visualization_manager import VisualizationManager, render_scene

__all__ = [
    # Base classes
    'BaseRenderer',
    'RenderConfig',
    'RenderResult',
    'RenderQuality',
    'VisualizationType',
    
    # Renderers
    'ManimRenderer',
    'MatplotlibRenderer',
    'PlotlyRenderer',
    
    # Manager
    'VisualizationManager',
    'render_scene',
    
    # Exceptions
    'RendererError',
    'RenderTimeoutError',
    'InvalidSceneDataError',
    'RenderingFailedError'
]

# Made with Bob