"""
Matplotlib renderer for graphs, plots, and data visualizations.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import time
import tempfile
from .base_renderer import (
    BaseRenderer, RenderResult, RenderConfig,
    InvalidSceneDataError, RenderingFailedError
)


class MatplotlibRenderer(BaseRenderer):
    """Renderer for Matplotlib graphs and plots."""
    
    def __init__(self, config: Optional[RenderConfig] = None):
        """Initialize Matplotlib renderer."""
        super().__init__(config)
    
    def render(self, scene_data: Dict[str, Any], output_path: Path) -> RenderResult:
        """
        Render Matplotlib visualization to video.
        
        Args:
            scene_data: Scene data with plot configuration
            output_path: Output video path
            
        Returns:
            RenderResult with rendering outcome
        """
        start_time = time.time()
        
        try:
            # Ensure output path has correct extension
            if output_path.suffix.lower() != '.mp4':
                output_path = output_path.with_suffix('.mp4')
            
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
            import numpy as np
            
            # Validate scene data
            validation = self.validate_scene(scene_data)
            if not validation["valid"]:
                return RenderResult(
                    success=False,
                    error=f"Invalid scene data: {validation['errors']}"
                )
            
            # Get plot code or generate default
            plot_code = scene_data.get("matplotlib_code") or scene_data.get("visualization_code")
            
            if plot_code:
                # Execute custom code
                result = self._render_custom_code(plot_code, scene_data, output_path)
            else:
                # Generate default visualization
                result = self._render_default_plot(scene_data, output_path)
            
            duration = time.time() - start_time
            
            if result["success"]:
                return RenderResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    metadata={
                        "renderer": "matplotlib",
                        "dpi": self.config.width // 10,
                        "fps": self.config.fps
                    }
                )
            else:
                return RenderResult(
                    success=False,
                    error=result["error"],
                    duration=duration
                )
                
        except ImportError:
            return RenderResult(
                success=False,
                error="Matplotlib not installed. Install with: pip install matplotlib"
            )
        except Exception as e:
            return RenderResult(
                success=False,
                error=f"Matplotlib rendering failed: {str(e)}",
                duration=time.time() - start_time
            )
    
    def preview(self, scene_data: Dict[str, Any]) -> RenderResult:
        """Generate quick preview."""
        # Generate preview path
        preview_path = self.output_dir / f"preview_{int(time.time())}.mp4"
        
        # Render with lower FPS for faster preview
        original_fps = self.config.fps
        self.config.fps = 15
        
        result = self.render(scene_data, preview_path)
        
        # Restore FPS
        self.config.fps = original_fps
        
        return result
    
    def validate_scene(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Matplotlib scene data."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check duration
        duration = scene_data.get("duration", 0)
        if duration <= 0:
            validation["errors"].append("Duration must be positive")
            validation["valid"] = False
        
        # Check for code or data
        has_code = bool(
            scene_data.get("matplotlib_code") or 
            scene_data.get("visualization_code")
        )
        has_data = bool(scene_data.get("plot_data"))
        
        if not has_code and not has_data:
            validation["warnings"].append(
                "No plot code or data provided, will use default visualization"
            )
        
        return validation
    
    def get_supported_features(self) -> list:
        """Get supported Matplotlib features."""
        return [
            "line_plots",
            "scatter_plots",
            "bar_charts",
            "histograms",
            "contour_plots",
            "heatmaps",
            "3d_plots",
            "animations",
            "subplots"
        ]
    
    def _render_custom_code(
        self,
        code: str,
        scene_data: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Render using custom Matplotlib code."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
            import numpy as np
            
            # Create figure
            fig, ax = plt.subplots(
                figsize=(self.config.width/100, self.config.height/100),
                dpi=100
            )
            
            # Prepare namespace for code execution
            namespace = {
                'plt': plt,
                'ax': ax,
                'fig': fig,
                'np': np,
                'animation': animation,
                'scene_data': scene_data
            }
            
            # Execute user code
            exec(code, namespace)
            
            # Check if animation was created
            if 'anim' in namespace:
                # Save animation
                anim = namespace['anim']
                duration = scene_data.get("duration", 5)
                frames = int(duration * self.config.fps)
                
                anim.save(
                    str(output_path),
                    writer='ffmpeg',
                    fps=self.config.fps,
                    dpi=100
                )
            else:
                # Static plot - convert to video
                self._static_to_video(fig, output_path, scene_data.get("duration", 5))
            
            plt.close(fig)
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _render_default_plot(
        self,
        scene_data: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Render default visualization based on scene data."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
            import numpy as np
            
            # Create figure
            fig, ax = plt.subplots(
                figsize=(self.config.width/100, self.config.height/100),
                dpi=100
            )
            
            # Get scene info
            title = scene_data.get("title", "Visualization")
            duration = scene_data.get("duration", 5)
            
            # Generate sample data
            x = np.linspace(0, 10, 100)
            
            # Create animated line plot
            line, = ax.plot([], [], 'b-', linewidth=2)
            ax.set_xlim(0, 10)
            ax.set_ylim(-1.5, 1.5)
            ax.set_title(title, fontsize=16)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.grid(True, alpha=0.3)
            
            def init():
                line.set_data([], [])
                return line,
            
            def animate(frame):
                # Animate a sine wave
                phase = frame / (self.config.fps * duration) * 4 * np.pi
                y = np.sin(x + phase)
                line.set_data(x, y)
                return line,
            
            frames = int(duration * self.config.fps)
            anim = animation.FuncAnimation(
                fig, animate, init_func=init,
                frames=frames, interval=1000/self.config.fps,
                blit=True
            )
            
            # Save animation with proper FFmpeg configuration
            try:
                from matplotlib.animation import FFMpegWriter
                writer = FFMpegWriter(
                    fps=self.config.fps,
                    codec='libx264',
                    bitrate=2000
                )
                # Set extra_args via metadata if supported
                writer.extra_args = ['-pix_fmt', 'yuv420p']
                anim.save(str(output_path), writer=writer, dpi=100)
            except Exception as e:
                # Fallback to simpler save method
                try:
                    anim.save(
                        str(output_path),
                        writer='ffmpeg',
                        fps=self.config.fps,
                        dpi=100
                    )
                except Exception as e2:
                    # Last resort: use pillow writer
                    anim.save(
                        str(output_path),
                        writer='pillow',
                        fps=self.config.fps,
                        dpi=100
                    )
            
            plt.close(fig)
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _static_to_video(self, fig, output_path: Path, duration: float):
        """Convert static plot to video by holding the frame."""
        import matplotlib.animation as animation
        
        def animate(frame):
            return []
        
        frames = int(duration * self.config.fps)
        anim = animation.FuncAnimation(
            fig, animate,
            frames=frames,
            interval=1000/self.config.fps
        )
        
        anim.save(
            str(output_path),
            writer='ffmpeg',
            fps=self.config.fps,
            dpi=100
        )


# Made with Bob