"""
Manim renderer for mathematical animations.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import subprocess
import tempfile
import time
import os
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
        import re
        
        # Sanitize scene name - remove all non-alphanumeric characters
        scene_title = scene_data.get("title", "CustomScene")
        # Remove special characters and keep only letters and numbers
        scene_name = re.sub(r'[^a-zA-Z0-9]', '', scene_title)
        # Ensure it starts with a letter
        if not scene_name or not scene_name[0].isalpha():
            scene_name = "Scene" + scene_name
        # Limit length
        scene_name = scene_name[:50]
        
        duration = scene_data.get("duration", 5)
        
        # Check if code already has a Scene class
        if "class" in code and "Scene" in code:
            # Code already has scene definition, but sanitize class names
            # Find and fix any invalid class names in the code
            code = re.sub(r'class\s+([^(:\s]+)[:\s]+', lambda m: f'class {re.sub(r"[^a-zA-Z0-9]", "", m.group(1))} ', code)
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
        """Generate professional 3Blue1Brown-style Manim scene."""
        title = scene_data.get("title", "Scene")
        visual_elements = scene_data.get("visual_elements", [])
        teaching_points = scene_data.get("teaching_points", [])
        animation_desc = scene_data.get("animation_description", "")
        
        # Detect if this is a mathematical concept
        is_math = any(keyword in title.lower() for keyword in
                     ['equation', 'formula', 'function', 'graph', 'calculus', 'algebra',
                      'geometry', 'vector', 'matrix', 'derivative', 'integral'])
        
        # 3Blue1Brown color scheme
        code = f"""
# 3Blue1Brown Professional Color Scheme
BG_COLOR = "#0C0C0C"  # Near black
PRIMARY_COLOR = "#58C4DD"  # 3B1B signature blue
SECONDARY_COLOR = "#83C167"  # Green
ACCENT_COLOR = "#FC6255"  # Red/Pink
TEXT_COLOR = "#ECECEC"  # Light gray
HIGHLIGHT_COLOR = "#FFFF00"  # Yellow
GRID_COLOR = "#404040"  # Dark gray

# Set background
self.camera.background_color = BG_COLOR

# === PROFESSIONAL TITLE (3Blue1Brown style) ===
title = Text("{title}", font_size=48, color=PRIMARY_COLOR, weight=BOLD)
title.to_edge(UP, buff=0.5)

# Smooth entrance
self.play(Write(title), run_time=1.5, rate_func=smooth)

# Elegant underline
underline = Line(
    title.get_left() + DOWN * 0.2,
    title.get_right() + DOWN * 0.2,
    color=ACCENT_COLOR,
    stroke_width=3
)
self.play(Create(underline), run_time=1, rate_func=smooth)
self.wait(0.8)

"""
        
        # Add mathematical content if detected
        if is_math:
            code += self._generate_math_content(title, visual_elements)
        else:
            code += self._generate_concept_content(title, visual_elements)
        
        # Add teaching points section
        if teaching_points:
            code += self._generate_teaching_points_section(teaching_points)
        
        # Professional closing
        code += """
# === PROFESSIONAL CLOSING ===
# Clear all elements
self.play(
    *[FadeOut(mob) for mob in self.mobjects],
    run_time=1.5
)

# Final message
final = Text("Remember This!", font_size=40, color=HIGHLIGHT_COLOR, weight=BOLD)
final.move_to(ORIGIN)
self.play(Write(final), run_time=1.5)
self.play(
    final.animate.scale(1.2),
    rate_func=there_and_back,
    run_time=1
)
self.wait(0.5)
self.play(FadeOut(final), run_time=1)
"""
        return code
    
    def _generate_math_content(self, title: str, elements: List[str]) -> str:
        """Generate mathematical visualization content."""
        return """
# === MATHEMATICAL CONTENT (3Blue1Brown style) ===
# Clear title for content
self.play(
    FadeOut(title),
    FadeOut(underline),
    run_time=1
)

# Create coordinate system
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 8, 2],
    x_length=8,
    y_length=5,
    axis_config={"color": GRID_COLOR, "stroke_width": 2},
    tips=True
)
axis_labels = axes.get_axis_labels(
    x_label=MathTex("x", color=TEXT_COLOR),
    y_label=MathTex("y", color=TEXT_COLOR)
)

self.play(Create(axes), Write(axis_labels), run_time=2, rate_func=smooth)
self.wait(0.5)

# Show equation
equation = MathTex("f(x) = x^2", color=PRIMARY_COLOR, font_size=44)
equation.to_edge(UP, buff=0.5)
self.play(Write(equation), run_time=1.5)
self.wait(0.5)

# Plot function
graph = axes.plot(
    lambda x: x**2,
    color=PRIMARY_COLOR,
    stroke_width=4
)
self.play(Create(graph), run_time=2.5, rate_func=smooth)
self.wait(0.8)

# Highlight a point
point_x = 2
point = Dot(axes.c2p(point_x, point_x**2), color=ACCENT_COLOR, radius=0.12)
point_label = MathTex(f"({point_x}, {point_x**2})", color=ACCENT_COLOR, font_size=32)
point_label.next_to(point, UR, buff=0.2)

self.play(
    GrowFromCenter(point),
    Write(point_label),
    run_time=1.5
)
self.wait(0.8)

# Add tangent line
slope = 2 * point_x
tangent = axes.plot(
    lambda x: slope * (x - point_x) + point_x**2,
    color=SECONDARY_COLOR,
    stroke_width=3,
    x_range=[point_x - 1.5, point_x + 1.5]
)
tangent_label = MathTex("\\\\text{Tangent}", color=SECONDARY_COLOR, font_size=28)
tangent_label.next_to(tangent, RIGHT, buff=0.3).shift(UP * 0.5)

self.play(Create(tangent), Write(tangent_label), run_time=1.5)
self.wait(1)

# Pulse effect for emphasis
self.play(
    point.animate.scale(1.5).set_color(HIGHLIGHT_COLOR),
    run_time=0.5
)
self.play(
    point.animate.scale(1/1.5).set_color(ACCENT_COLOR),
    run_time=0.5
)
self.wait(0.5)

"""
    
    def _generate_concept_content(self, title: str, elements: List[str]) -> str:
        """Generate conceptual visualization content."""
        code = """
# === CONCEPTUAL CONTENT (3Blue1Brown style) ===
# Clear title
self.play(
    FadeOut(title),
    FadeOut(underline),
    run_time=1
)

"""
        
        # Add visual elements with engaging animations
        if elements:
            code += """
# === MAIN CONTENT: Visual elements with animations ===

"""
            for i, element in enumerate(elements[:3]):
                # Escape quotes in element text
                element_safe = element.replace('"', '\\"')
                
                code += f"""
# Element {i+1}: {element_safe[:30]}...
elem_{i} = Text("{element_safe[:60]}", font_size=40, color=WHITE)
elem_{i}.move_to(ORIGIN)

# Create visual icon/shape
icon_{i} = Circle(radius=0.5, color=PRIMARY_COLOR, fill_opacity=0.3)
icon_{i}.next_to(elem_{i}, LEFT, buff=0.5)

# Animate entrance
self.play(
    FadeIn(icon_{i}, scale=0.5),
    Write(elem_{i}),
    run_time=1
)

# Add emphasis with pulse effect
self.play(
    icon_{i}.animate.scale(1.2).set_color(ACCENT_COLOR),
    rate_func=there_and_back,
    run_time=0.5
)

self.wait(0.8)

# Transition out
self.play(
    FadeOut(elem_{i}, shift=UP),
    FadeOut(icon_{i}, scale=0.5),
    run_time=0.6
)

"""
        return code
    
    def _generate_teaching_points_section(self, teaching_points: List[str]) -> str:
        """Generate teaching points section with professional styling."""
        code = """
# === KEY POINTS (3Blue1Brown style) ===
"""
        for idx, point in enumerate(teaching_points[:3]):
            # Escape quotes and limit length
            point_safe = point.replace('"', '\\"')[:80]
            
            # Calculate vertical position for this point
            y_position = 1 - idx * 0.8
            
            code += f"""
# Teaching Point {idx+1}
bullet_{idx} = Dot(color=ACCENT_COLOR, radius=0.12)
bullet_{idx}.to_edge(LEFT, buff=1).shift(UP * {y_position})

point_{idx} = Text(
    "{point_safe}",
    font_size=32,
    color=TEXT_COLOR,
    line_spacing=1.2
)
point_{idx}.next_to(bullet_{idx}, RIGHT, buff=0.3)
point_{idx}.align_to(bullet_{idx}, UP)

self.play(GrowFromCenter(bullet_{idx}), run_time=0.5)
self.play(Write(point_{idx}), run_time=1.2, rate_func=smooth)

check_{idx} = Text("✓", font_size=36, color=SECONDARY_COLOR)
check_{idx}.next_to(point_{idx}, RIGHT, buff=0.3)
self.play(FadeIn(check_{idx}, scale=0.5), run_time=0.6)
self.wait(0.8)

"""
        return code
    
    def _generate_closing(self) -> str:
        """Generate professional closing."""
        return """
# === PROFESSIONAL CLOSING ===
self.play(
    *[FadeOut(mob) for mob in self.mobjects],
    run_time=1.5
)

final_text = Text("Remember This!", font_size=48, color=HIGHLIGHT_COLOR, weight=BOLD)
final_text.move_to(ORIGIN)

# Dramatic entrance
self.play(
    Write(final_text),
    run_time=1
)

# Pulse effect for emphasis
self.play(
    final_text.animate.scale(1.2),
    rate_func=there_and_back,
    run_time=0.6
)

self.wait(0.5)

# Fade out
self.play(
    FadeOut(final_text),
    run_time=0.5
)
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
            env = os.environ.copy()
            env['OPENBLAS_NUM_THREADS'] = '1'  # Limit threads to reduce memory
            env['OMP_NUM_THREADS'] = '1'
            env['MKL_NUM_THREADS'] = '1'
            
            # Run Manim with retry logic and longer timeout
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=600,  # 10 minute timeout (increased for complex animations)
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
                    
                    # Get full error message but format it better
                    error_lines = result.stderr.split('\n')
                    # Get last 10 lines which usually contain the actual error
                    relevant_error = '\n'.join(error_lines[-10:]) if len(error_lines) > 10 else result.stderr
                    
                    return {
                        "success": False,
                        "error": f"Manim error: {relevant_error[:1000]}"  # Show more context
                    }
                    
                except subprocess.TimeoutExpired:
                    if attempt < max_retries - 1:
                        continue
                    return {
                        "success": False,
                        "error": "Manim rendering timed out (10 minutes). Try reducing scene complexity or duration."
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