"""
Plotly renderer for 3D and interactive visualizations.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import time
from .base_renderer import (
    BaseRenderer, RenderResult, RenderConfig,
    InvalidSceneDataError, RenderingFailedError
)


class PlotlyRenderer(BaseRenderer):
    """Renderer for Plotly 3D and interactive visualizations."""
    
    def __init__(self, config: Optional[RenderConfig] = None):
        """Initialize Plotly renderer."""
        super().__init__(config)
    
    def render(self, scene_data: Dict[str, Any], output_path: Path) -> RenderResult:
        """
        Render Plotly visualization to video.
        
        Args:
            scene_data: Scene data with Plotly configuration
            output_path: Output video path
            
        Returns:
            RenderResult with rendering outcome
        """
        start_time = time.time()
        
        try:
            # Ensure output path has correct extension
            if output_path.suffix.lower() != '.mp4':
                output_path = output_path.with_suffix('.mp4')
            
            import plotly.graph_objects as go
            import plotly.io as pio
            import numpy as np
            from PIL import Image
            import io
            
            # Validate scene data
            validation = self.validate_scene(scene_data)
            if not validation["valid"]:
                return RenderResult(
                    success=False,
                    error=f"Invalid scene data: {validation['errors']}"
                )
            
            # Get Plotly code or generate default
            plotly_code = scene_data.get("plotly_code") or scene_data.get("visualization_code")
            
            if plotly_code:
                # Execute custom code
                result = self._render_custom_code(plotly_code, scene_data, output_path)
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
                        "renderer": "plotly",
                        "width": self.config.width,
                        "height": self.config.height,
                        "fps": self.config.fps
                    }
                )
            else:
                return RenderResult(
                    success=False,
                    error=result["error"],
                    duration=duration
                )
                
        except ImportError as e:
            return RenderResult(
                success=False,
                error=f"Required library not installed: {str(e)}\nInstall with: pip install plotly kaleido pillow"
            )
        except Exception as e:
            return RenderResult(
                success=False,
                error=f"Plotly rendering failed: {str(e)}",
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
        """Validate Plotly scene data."""
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
            scene_data.get("plotly_code") or 
            scene_data.get("visualization_code")
        )
        has_data = bool(scene_data.get("plot_data"))
        
        if not has_code and not has_data:
            validation["warnings"].append(
                "No plot code or data provided, will use default visualization"
            )
        
        return validation
    
    def get_supported_features(self) -> list:
        """Get supported Plotly features."""
        return [
            "3d_surface_plots",
            "3d_scatter_plots",
            "vector_fields",
            "contour_plots",
            "mesh_plots",
            "parametric_plots",
            "animations",
            "interactive_plots"
        ]
    
    def _render_custom_code(
        self,
        code: str,
        scene_data: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Render using custom Plotly code."""
        try:
            import plotly.graph_objects as go
            import plotly.io as pio
            import numpy as np
            
            # Prepare namespace for code execution
            namespace = {
                'go': go,
                'pio': pio,
                'np': np,
                'scene_data': scene_data
            }
            
            # Execute user code
            exec(code, namespace)
            
            # Get the figure
            if 'fig' not in namespace:
                return {"success": False, "error": "Code must create a 'fig' variable"}
            
            fig = namespace['fig']
            
            # Render to video
            self._figure_to_video(fig, output_path, scene_data.get("duration", 5))
            
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _render_default_plot(
        self,
        scene_data: Dict[str, Any],
        output_path: Path
    ) -> Dict[str, Any]:
        """Render default 3D visualization."""
        try:
            import plotly.graph_objects as go
            import numpy as np
            
            # Get scene info
            title = scene_data.get("title", "3D Visualization")
            duration = scene_data.get("duration", 5)
            
            # Create sample 3D surface
            x = np.linspace(-5, 5, 50)
            y = np.linspace(-5, 5, 50)
            X, Y = np.meshgrid(x, y)
            Z = np.sin(np.sqrt(X**2 + Y**2))
            
            # Create figure
            fig = go.Figure(data=[go.Surface(
                x=X, y=Y, z=Z,
                colorscale='Viridis',
                showscale=True
            )])
            
            fig.update_layout(
                title=title,
                scene=dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z',
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5)
                    )
                ),
                width=self.config.width,
                height=self.config.height
            )
            
            # Render to video
            self._figure_to_video(fig, output_path, duration)
            
            return {"success": True}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _figure_to_video(self, fig, output_path: Path, duration: float):
        """Convert Plotly figure to video with rotation animation."""
        import plotly.io as pio
        from PIL import Image
        import subprocess
        import tempfile
        import numpy as np
        
        # Check if kaleido is available
        try:
            import kaleido
            has_kaleido = True
        except ImportError:
            has_kaleido = False
        
        if not has_kaleido:
            # Try to use orca as fallback
            try:
                pio.orca.config.executable = 'orca'
                pio.orca.status
                use_orca = True
            except:
                use_orca = False
            
            if not use_orca:
                raise ImportError(
                    "Plotly image export requires either Kaleido or Orca.\n"
                    "Install Kaleido with: pip install kaleido\n"
                    "Or install Orca from: https://github.com/plotly/orca"
                )
        
        # Calculate frames
        frames = int(duration * self.config.fps)
        
        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Generate frames with rotation
            for i in range(frames):
                # Calculate rotation angle
                angle = (i / frames) * 360
                
                # Update camera position for rotation
                eye_x = 1.5 * np.cos(np.radians(angle))
                eye_y = 1.5 * np.sin(np.radians(angle))
                
                fig.update_layout(
                    scene_camera=dict(
                        eye=dict(x=eye_x, y=eye_y, z=1.5)
                    )
                )
                
                # Save frame as image
                frame_path = temp_path / f"frame_{i:04d}.png"
                try:
                    pio.write_image(
                        fig,
                        str(frame_path),
                        width=self.config.width,
                        height=self.config.height,
                        format='png'
                    )
                except Exception as e:
                    raise RuntimeError(f"Failed to export frame {i}: {str(e)}")
            
            # Convert frames to video using ffmpeg
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-framerate', str(self.config.fps),
                '-i', str(temp_path / 'frame_%04d.png'),
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                '-crf', '23',
                str(output_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")


# Made with Bob