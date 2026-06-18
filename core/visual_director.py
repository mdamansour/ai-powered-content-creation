"""
Visual Director AI - Plans rich visual content with minimal text.
This is the FIRST stage in the visual-first pipeline.
"""
from typing import Dict, Any, List, Optional


class VisualDirector:
    """
    AI Director that plans visual storytelling with rich diagrams, animations,
    and interactive elements. Focuses on SHOWING not TELLING.
    """
    
    def __init__(self, ai_engine):
        """
        Initialize Visual Director.
        
        Args:
            ai_engine: AI engine instance for generation
        """
        self.ai_engine = ai_engine
    
    def plan_visual_story(
        self,
        research_data: Dict[str, Any],
        duration: int = 300,
        style: str = "3blue1brown"
    ) -> Dict[str, Any]:
        """
        Plan a visual story with rich diagrams and minimal text.
        
        Args:
            research_data: Research findings about the topic
            duration: Target duration in seconds
            style: Visual style ('3blue1brown', 'modern', 'minimal')
            
        Returns:
            Dict with visual story plan
        """
        prompt = self._build_director_prompt(research_data, duration, style)
        
        try:
            response = self.ai_engine.generate(prompt)
            visual_plan = self.ai_engine._parse_json_response(response)
            
            if visual_plan.get("parsed") == False:
                return {
                    "success": False,
                    "error": "Failed to parse visual plan",
                    "raw": response
                }
            
            return {
                "success": True,
                "visual_plan": visual_plan,
                "style": style,
                "duration": duration
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_director_prompt(
        self,
        research_data: Dict[str, Any],
        duration: int,
        style: str
    ) -> str:
        """Build prompt for Visual Director AI."""
        
        title = research_data.get("title", "Unknown Topic")
        concepts = research_data.get("concepts", [])
        formulas = research_data.get("formulas", [])
        principles = research_data.get("principles", [])
        
        # Extract key visual elements
        concept_names = [c.get("name", "") for c in concepts[:5]]
        formula_list = [f.get("latex", "") for f in formulas[:3]]
        
        return f"""
You are a VISUAL DIRECTOR for educational content, like a film director planning shots.
Your job is to plan RICH VISUAL CONTENT with MINIMAL TEXT.

Topic: {title}
Duration: {duration} seconds
Style: {style}

Key Concepts: {', '.join(concept_names)}
Key Formulas: {', '.join(formula_list)}

=== YOUR MISSION ===
Plan a visual story that SHOWS the concept through:
- Diagrams and geometric constructions
- Animated transformations
- Interactive demonstrations
- Visual metaphors
- Color-coded elements
- Dynamic graphs and plots

=== CRITICAL RULES ===
1. **VISUALS FIRST**: 80% visuals, 20% text maximum
2. **SHOW DON'T TELL**: Use diagrams, not bullet points
3. **RICH CONTENT**: Every scene must have multiple visual elements
4. **MINIMAL TEXT**: Only essential labels and equations
5. **INTERACTIVE**: Elements should move, transform, interact
6. **PROGRESSIVE**: Build complexity visually step-by-step

=== VISUAL ELEMENTS TO USE ===

**Mathematical Concepts:**
- Coordinate systems (Axes, NumberPlane)
- Function graphs with animations
- Geometric shapes with transformations
- Equation morphing (Transform)
- Vector fields and arrows
- 3D objects and rotations

**Physics Concepts:**
- Force diagrams with vectors
- Motion paths and trajectories
- Energy flow visualizations
- Field lines and gradients
- Particle systems
- Wave animations

**Abstract Concepts:**
- Visual metaphors (e.g., water flow for current)
- Color-coded categories
- Size/scale comparisons
- Before/after transformations
- Cause-effect chains
- Network diagrams

=== EXAMPLE: BAD vs GOOD ===

❌ BAD (Text-heavy):
```
Scene 1: "Introduction to Quadratic Equations"
- Show title
- List 3 bullet points about properties
- Show formula
```

✅ GOOD (Visual-rich):
```
Scene 1: "Parabola Emergence"
Visual Elements:
- Start with coordinate axes (animated creation)
- Plot points one by one forming parabola shape
- Connect points with smooth curve (Create animation)
- Show equation emerging from the curve
- Highlight vertex with pulsing dot
- Show axis of symmetry as dashed line
- Animate tangent line sliding along curve
- Color-code: curve (blue), vertex (red), tangent (green)
Text: Only "f(x) = x²" equation label
```

=== OUTPUT FORMAT ===

Return a JSON with 5-8 visual scenes:

{{
  "title": "{title}",
  "total_duration": {duration},
  "visual_style": "{style}",
  "color_palette": {{
    "primary": "#58C4DD",
    "secondary": "#83C167",
    "accent": "#FC6255",
    "background": "#0C0C0C"
  }},
  "scenes": [
    {{
      "scene_number": 1,
      "title": "Short descriptive title",
      "duration": 40,
      "visual_concept": "What visual story this scene tells",
      "primary_visual_elements": [
        "Coordinate axes with grid",
        "Animated function graph",
        "Highlighted critical points",
        "Tangent line animation"
      ],
      "manim_objects": [
        "Axes",
        "Graph",
        "Dot",
        "Line",
        "MathTex",
        "Arrow"
      ],
      "animations": [
        "Create(axes)",
        "Create(graph)",
        "GrowFromCenter(point)",
        "Transform(line1, line2)"
      ],
      "color_scheme": {{
        "main_object": "primary",
        "highlights": "accent",
        "labels": "secondary"
      }},
      "text_elements": [
        "f(x) = x²"
      ],
      "visual_flow": "Axes appear → Graph draws → Point highlights → Tangent slides",
      "teaching_goal": "Show parabola shape visually"
    }},
    {{
      "scene_number": 2,
      "title": "Next visual concept",
      ...
    }}
  ]
}}

=== REQUIREMENTS ===
✓ 5-8 scenes total
✓ Each scene: 30-60 seconds
✓ Rich visual elements (5+ per scene)
✓ Minimal text (1-3 labels max)
✓ Specific Manim objects listed
✓ Clear animation sequence
✓ Color-coded elements
✓ Visual flow description
✓ Total duration = {duration} seconds

Focus on VISUAL STORYTELLING. Make it look like a 3Blue1Brown video!

Return ONLY valid JSON.
"""
    
    def validate_visual_plan(self, visual_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that visual plan has rich content.
        
        Args:
            visual_plan: Visual plan to validate
            
        Returns:
            Dict with validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "richness_score": 0
        }
        
        scenes = visual_plan.get("scenes", [])
        
        if not scenes:
            validation["valid"] = False
            validation["errors"].append("No scenes in visual plan")
            return validation
        
        total_visual_elements = 0
        total_text_elements = 0
        
        for i, scene in enumerate(scenes, 1):
            # Check for visual elements
            visual_elements = scene.get("primary_visual_elements", [])
            text_elements = scene.get("text_elements", [])
            
            total_visual_elements += len(visual_elements)
            total_text_elements += len(text_elements)
            
            if len(visual_elements) < 3:
                validation["warnings"].append(
                    f"Scene {i}: Only {len(visual_elements)} visual elements (recommend 5+)"
                )
            
            if len(text_elements) > 5:
                validation["warnings"].append(
                    f"Scene {i}: Too much text ({len(text_elements)} elements)"
                )
            
            # Check for Manim objects
            if not scene.get("manim_objects"):
                validation["errors"].append(
                    f"Scene {i}: No Manim objects specified"
                )
                validation["valid"] = False
            
            # Check for animations
            if not scene.get("animations"):
                validation["warnings"].append(
                    f"Scene {i}: No animations specified"
                )
        
        # Calculate richness score (0-100)
        avg_visuals_per_scene = total_visual_elements / len(scenes) if scenes else 0
        avg_text_per_scene = total_text_elements / len(scenes) if scenes else 0
        
        # Good: 5+ visuals, <3 text per scene
        visual_score = min(100, (avg_visuals_per_scene / 5) * 70)
        text_penalty = max(0, (avg_text_per_scene - 3) * 10)
        
        validation["richness_score"] = int(max(0, visual_score - text_penalty))
        
        if validation["richness_score"] < 50:
            validation["warnings"].append(
                f"Low visual richness score: {validation['richness_score']}/100"
            )
        
        return validation


# Made with Bob