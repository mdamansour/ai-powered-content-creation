"""
Scenario Composer - Converts visual plans into detailed executable Manim code.
This is the SECOND stage in the visual-first pipeline.
"""
from typing import Dict, Any, List, Optional


class ScenarioComposer:
    """
    Composes detailed Manim scenes from visual plans.
    Takes rich visual descriptions and generates executable code.
    """
    
    def __init__(self, ai_engine):
        """
        Initialize Scenario Composer.
        
        Args:
            ai_engine: AI engine instance for code generation
        """
        self.ai_engine = ai_engine
    
    def compose_scenes(
        self,
        visual_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compose detailed Manim scenes from visual plan.
        
        Args:
            visual_plan: Visual plan from Visual Director
            
        Returns:
            Dict with detailed scenes including Manim code
        """
        if not visual_plan.get("scenes"):
            return {
                "success": False,
                "error": "No scenes in visual plan"
            }
        
        composed_scenes = []
        
        for scene_plan in visual_plan["scenes"]:
            prompt = self._build_composer_prompt(scene_plan, visual_plan)
            
            try:
                response = self.ai_engine.generate(prompt)
                scene_code = self.ai_engine._parse_json_response(response)
                
                if scene_code.get("parsed") != False:
                    composed_scenes.append(scene_code)
                else:
                    # Fallback: use scene plan as-is
                    composed_scenes.append(scene_plan)
                    
            except Exception as e:
                print(f"Error composing scene {scene_plan.get('scene_number')}: {e}")
                composed_scenes.append(scene_plan)
        
        return {
            "success": True,
            "total_duration": visual_plan.get("total_duration"),
            "scenes": composed_scenes,
            "visual_style": visual_plan.get("visual_style"),
            "color_palette": visual_plan.get("color_palette")
        }
    
    def _build_composer_prompt(
        self,
        scene_plan: Dict[str, Any],
        visual_plan: Dict[str, Any]
    ) -> str:
        """Build prompt for composing detailed Manim code."""
        
        scene_num = scene_plan.get("scene_number", 1)
        title = scene_plan.get("title", "Scene")
        duration = scene_plan.get("duration", 30)
        visual_elements = scene_plan.get("primary_visual_elements", [])
        manim_objects = scene_plan.get("manim_objects", [])
        animations = scene_plan.get("animations", [])
        visual_flow = scene_plan.get("visual_flow", "")
        color_scheme = scene_plan.get("color_scheme", {})
        text_elements = scene_plan.get("text_elements", [])
        
        # Get color palette
        palette = visual_plan.get("color_palette", {})
        
        return f"""
You are a MANIM CODE COMPOSER. Convert this visual plan into COMPLETE, EXECUTABLE Manim code.

=== SCENE PLAN ===
Scene {scene_num}: {title}
Duration: {duration} seconds
Visual Flow: {visual_flow}

Visual Elements to Create:
{chr(10).join(f"- {elem}" for elem in visual_elements)}

Manim Objects to Use:
{', '.join(manim_objects)}

Animations to Include:
{chr(10).join(f"- {anim}" for anim in animations)}

Text Elements (MINIMAL):
{chr(10).join(f"- {text}" for text in text_elements)}

Color Scheme:
- Primary: {palette.get('primary', '#58C4DD')}
- Secondary: {palette.get('secondary', '#83C167')}
- Accent: {palette.get('accent', '#FC6255')}
- Background: {palette.get('background', '#0C0C0C')}
- Text: #ECECEC

=== YOUR TASK ===
Generate COMPLETE, WORKING Manim code that:
1. Creates ALL visual elements listed above
2. Uses the specified Manim objects
3. Implements the animations in sequence
4. Follows the visual flow exactly
5. Uses the color scheme provided
6. Minimizes text (only essential labels)
7. Runs for approximately {duration} seconds

=== CODE REQUIREMENTS ===
✓ COMPLETE code (ready to execute in construct())
✓ Import statements if needed (numpy, etc.)
✓ All visual elements from the plan
✓ Smooth animations with proper timing
✓ Color-coded as specified
✓ Professional 3Blue1Brown style
✓ NO placeholder comments - REAL code only
✓ Proper wait() calls for timing

=== EXAMPLE OUTPUT ===
```python
# Set background
self.camera.background_color = "{palette.get('background', '#0C0C0C')}"

# Create coordinate axes
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 8, 2],
    x_length=8,
    y_length=5,
    axis_config={{"color": "#404040", "stroke_width": 2}},
    tips=True
)
axis_labels = axes.get_axis_labels(
    x_label=MathTex("x", color="#ECECEC"),
    y_label=MathTex("y", color="#ECECEC")
)

# Animate axes creation
self.play(Create(axes), run_time=1.5, rate_func=smooth)
self.play(Write(axis_labels), run_time=1)
self.wait(0.5)

# Create and plot function
func_eq = MathTex("f(x) = x^2", color="{palette.get('primary', '#58C4DD')}", font_size=44)
func_eq.to_edge(UP, buff=0.5)
self.play(Write(func_eq), run_time=1.5)

graph = axes.plot(
    lambda x: x**2,
    color="{palette.get('primary', '#58C4DD')}",
    stroke_width=4
)
self.play(Create(graph), run_time=2, rate_func=smooth)
self.wait(1)

# Highlight critical point
point = Dot(axes.c2p(0, 0), color="{palette.get('accent', '#FC6255')}", radius=0.12)
point_label = MathTex("(0, 0)", color="{palette.get('accent', '#FC6255')}", font_size=32)
point_label.next_to(point, DR, buff=0.2)

self.play(GrowFromCenter(point), Write(point_label), run_time=1.5)
self.wait(1)

# Pulse effect for emphasis
self.play(point.animate.scale(1.5).set_color("#FFFF00"), run_time=0.5)
self.play(point.animate.scale(1/1.5).set_color("{palette.get('accent', '#FC6255')}"), run_time=0.5)
self.wait(0.5)
```

=== OUTPUT FORMAT ===
Return JSON with:
{{
  "scene_number": {scene_num},
  "title": "{title}",
  "duration": {duration},
  "visualization_type": "manim",
  "manim_code": "COMPLETE EXECUTABLE CODE HERE (properly escaped)",
  "visual_elements": {visual_elements},
  "animation_description": "{visual_flow}",
  "teaching_points": ["Key point 1", "Key point 2"],
  "transition": "Fade out all elements"
}}

CRITICAL: The manim_code field must contain COMPLETE, WORKING Python code that can be executed directly in a Manim Scene's construct() method. NO placeholders, NO comments saying "add code here" - REAL, FUNCTIONAL code only!

Return ONLY valid JSON with complete Manim code.
"""
    
    def validate_composed_scene(self, scene: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that composed scene has executable code.
        
        Args:
            scene: Composed scene to validate
            
        Returns:
            Dict with validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check for manim_code
        manim_code = scene.get("manim_code", "")
        if not manim_code:
            validation["valid"] = False
            validation["errors"].append("No Manim code provided")
            return validation
        
        # Check code quality
        if len(manim_code) < 100:
            validation["warnings"].append("Manim code seems too short")
        
        # Check for placeholder comments
        placeholders = ["TODO", "add code here", "implement", "placeholder"]
        for placeholder in placeholders:
            if placeholder.lower() in manim_code.lower():
                validation["warnings"].append(
                    f"Code contains placeholder: '{placeholder}'"
                )
        
        # Check for essential Manim patterns
        essential_patterns = ["self.play", "self.wait"]
        missing = [p for p in essential_patterns if p not in manim_code]
        if missing:
            validation["warnings"].append(
                f"Code missing essential patterns: {', '.join(missing)}"
            )
        
        # Check for visual richness
        visual_keywords = [
            "Axes", "Graph", "Circle", "Square", "Vector", "Arrow",
            "MathTex", "Dot", "Line", "Create", "Transform", "FadeIn"
        ]
        found_keywords = [kw for kw in visual_keywords if kw in manim_code]
        
        if len(found_keywords) < 3:
            validation["warnings"].append(
                f"Low visual richness: only {len(found_keywords)} visual elements found"
            )
        
        return validation


# Made with Bob