"""
Manim renderer for mathematical animations.
"""
from typing import Dict, Any, Optional
from pathlib import Path
import subprocess
import tempfile
import time
from .base_renderer import (
    BaseRenderer, RenderResult, RenderConfig, 
    InvalidSceneDataError, RenderingFailedError
)


class ManimRenderer(BaseRenderer):
    """Renderer for Manim mathematical animations."""
    
    def __init__(self, config: Optional[RenderConfig] = None):
        """Initialize Manim renderer."""
        super().__init__(config)
        self.manim_quality_map = {
            "low": "l",      # Low quality (480p)
            "medium": "m",   # Medium quality (720p)
            "high": "h",     # High quality (1080p)
            "ultra": "k"     # 4K quality
        }
    
    def render(self, scene_data: Dict[str, Any], output_path: Path) -> RenderResult:
        """
        Render Manim scene to video.
        
        Args:
            scene_data: Scene data with Manim code
            output_path: Output video path
            
        Returns:
            RenderResult with rendering outcome
        """
        start_time = time.time()
        
        try:
            # Validate scene data
            validation = self.validate_scene(scene_data)
            if not validation["valid"]:
                return RenderResult(
                    success=False,
                    error=f"Invalid scene data: {validation['errors']}"
                )
            
            # Get Manim code
            manim_code = scene_data.get("manim_code") or scene_data.get("visualization_code")
            if not manim_code:
                # Generate default code if not provided
                manim_code = self._generate_default_scene(scene_data)
            
            # Create temporary Python file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                encoding='utf-8'
            ) as f:
                temp_file = Path(f.name)
                f.write(self._wrap_manim_code(manim_code, scene_data))
            
            # Render with Manim
            result = self._run_manim(temp_file, output_path)
            
            # Clean up
            temp_file.unlink()
            
            duration = time.time() - start_time
            
            if result["success"]:
                return RenderResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    metadata={
                        "renderer": "manim",
                        "quality": self.config.quality.value,
                        "fps": self.config.fps
                    }
                )
            else:
                return RenderResult(
                    success=False,
                    error=result["error"],
                    duration=duration
                )
                
        except Exception as e:
            return RenderResult(
                success=False,
                error=f"Manim rendering failed: {str(e)}",
                duration=time.time() - start_time
            )
    
    def preview(self, scene_data: Dict[str, Any]) -> RenderResult:
        """Generate quick preview with low quality."""
        # Save current config
        original_quality = self.config.quality
        
        # Use low quality for preview
        from .base_renderer import RenderQuality
        self.config.quality = RenderQuality.LOW
        
        # Generate preview path
        preview_path = self.output_dir / f"preview_{int(time.time())}.mp4"
        
        # Render
        result = self.render(scene_data, preview_path)
        
        # Restore config
        self.config.quality = original_quality
        
        return result
    
    def validate_scene(self, scene_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Manim scene data."""
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for code
        has_code = bool(
            scene_data.get("manim_code") or 
            scene_data.get("visualization_code")
        )
        
        if not has_code and not scene_data.get("visual_elements"):
            validation["warnings"].append(
                "No Manim code or visual elements provided, will use default scene"
            )
        
        # Check duration
        duration = scene_data.get("duration", 0)
        if duration <= 0:
            validation["errors"].append("Duration must be positive")
            validation["valid"] = False
        
        return validation
    
    def get_supported_features(self) -> list:
        """Get supported Manim features."""
        return [
            "equations",
            "transformations",
            "geometric_shapes",
            "graphs",
            "3d_objects",
            "text_animations",
            "vector_fields",
            "number_lines"
        ]
    
    def _wrap_manim_code(self, code: str, scene_data: Dict[str, Any]) -> str:
        """Wrap user code in proper Manim scene class."""
        scene_name = scene_data.get("title", "CustomScene").replace(" ", "")
        duration = scene_data.get("duration", 5)
        
        # Check if code already has a Scene class
        if "class" in code and "Scene" in code:
            # Code already has scene definition
            return f"""
from manim import *

{code}
"""
        
        # Wrap code in Scene class
        return f"""
from manim import *

class {scene_name}(Scene):
    def construct(self):
        # Scene duration: {duration} seconds
        {self._indent_code(code)}
        
        # Hold final frame
        self.wait(1)
"""
    
    def _indent_code(self, code: str, spaces: int = 8) -> str:
        """Indent code block."""
        lines = code.split('\n')
        return '\n'.join(' ' * spaces + line if line.strip() else line for line in lines)
    
    def _generate_default_scene(self, scene_data: Dict[str, Any]) -> str:
        """Generate default Manim scene from scene data."""
        title = scene_data.get("title", "Scene")
        visual_elements = scene_data.get("visual_elements", [])
        teaching_points = scene_data.get("teaching_points", [])
        
        code = f"""
# Title
title = Text("{title}", font_size=48)
self.play(Write(title))
self.wait(1)
self.play(FadeOut(title))

"""
        
        # Add visual elements
        if visual_elements:
            code += "# Visual elements\n"
            for i, element in enumerate(visual_elements[:3]):  # Limit to 3
                code += f"""
element_{i} = Text("{element}", font_size=36)
self.play(FadeIn(element_{i}))
self.wait(1)
"""
        
        # Add teaching points
        if teaching_points:
            code += "\n# Teaching points\n"
            for i, point in enumerate(teaching_points[:2]):  # Limit to 2
                code += f"""
point_{i} = Text("{point[:50]}", font_size=28)
point_{i}.to_edge(DOWN)
self.play(Write(point_{i}))
self.wait(2)
self.play(FadeOut(point_{i}))
"""
        
        return code
    
    def _run_manim(self, script_path: Path, output_path: Path) -> Dict[str, Any]:
        """Run Manim CLI to render scene with error recovery."""
        try:
            # Ensure output path has correct extension
            if output_path.suffix.lower() != '.mp4':
                output_path = output_path.with_suffix('.mp4')
            
            # Get quality flag
            quality_flag = self.manim_quality_map.get(
                self.config.quality.value,
                "m"
            )
            
            # Create a dedicated media directory for this render
            media_dir = output_path.parent / "media"
            media_dir.mkdir(parents=True, exist_ok=True)
            
            # Build command with OpenBLAS memory fix
            cmd = [
                "manim",
                "render",
                str(script_path),
                f"-q{quality_flag}",  # Quality
                f"--fps={self.config.fps}",
                f"--format={self.config.output_format}",
                f"-o", output_path.name,
                "--media_dir", str(media_dir)
            ]
            
            # Set environment variables to handle OpenBLAS memory issues
            env = subprocess.os.environ.copy()
            env['OPENBLAS_NUM_THREADS'] = '1'  # Limit threads to reduce memory
            env['OMP_NUM_THREADS'] = '1'
            env['MKL_NUM_THREADS'] = '1'
            
            # Run Manim with retry logic
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300,  # 5 minute timeout
                        env=env
                    )
                    
                    if result.returncode == 0:
                        # Find the actual output file from Manim's directory structure
                        # Manim creates: media_dir/videos/script_name/quality/output_name.mp4
                        import glob
                        
                        # Search for the output file
                        search_pattern = str(media_dir / "**" / output_path.name)
                        matches = glob.glob(search_pattern, recursive=True)
                        
                        if matches:
                            actual_output = Path(matches[0])
                            # Move to desired location
                            import shutil
                            shutil.move(str(actual_output), str(output_path))
                            return {"success": True, "output_path": output_path}
                        else:
                            # File might already be in the right place
                            if output_path.exists():
                                return {"success": True, "output_path": output_path}
                            return {
                                "success": False,
                                "error": f"Manim completed but output file not found at {output_path}"
                            }
                    
                    # Check for OpenBLAS memory error
                    if "OpenBLAS" in result.stderr and "Memory allocation" in result.stderr:
                        if attempt < max_retries - 1:
                            # Retry with even lower quality
                            if quality_flag != "l":
                                cmd[4] = "-ql"  # Force low quality
                                continue
                        return {
                            "success": False,
                            "error": "OpenBLAS memory error: Try reducing quality or closing other applications"
                        }
                    
                    return {
                        "success": False,
                        "error": f"Manim error: {result.stderr[:500]}"  # Limit error message length
                    }
                    
                except subprocess.TimeoutExpired:
                    if attempt < max_retries - 1:
                        continue
                    return {
                        "success": False,
                        "error": "Manim rendering timed out (5 minutes)"
                    }
                    
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Manim not found. Please install: pip install manim"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Manim execution failed: {str(e)}"
            }


# Made with Bob