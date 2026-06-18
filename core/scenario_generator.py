"""
Scenario generation for creating visualization scenes from research data.
"""
from typing import Dict, List, Optional, Any
from core.ai_engine import AIEngine
from utils.model_selector import ModelSelector


class ScenarioGenerator:
    """Generate visualization scenarios from research data."""
    
    def __init__(self, engine: Optional[AIEngine] = None):
        """
        Initialize scenario generator.
        
        Args:
            engine: Optional AI engine (creates one if not provided)
        """
        self.engine = engine or ModelSelector.get_engine_for_task("scenario")
    
    def generate_scenario(
        self,
        research: Dict[str, Any],
        target_duration: int = 300,
        scene_count: int = 5,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate visualization scenario from research data.
        
        Args:
            research: Research data dictionary
            target_duration: Target duration in seconds (default 5 minutes)
            scene_count: Desired number of scenes (default 5)
            custom_instructions: Optional additional instructions
            
        Returns:
            Dict containing scene-by-scene scenario
        """
        try:
            # Extract key concepts for scenario generation
            concepts = research.get("concepts", [])
            formulas = research.get("formulas", [])
            
            if not concepts:
                return {
                    "success": False,
                    "error": "No concepts found in research data",
                    "scenes": []
                }
            
            # Build scenario prompt
            prompt = self._build_scenario_prompt(
                research,
                target_duration,
                custom_instructions
            )
            
            # Generate scenario with specified scene count (synchronous)
            scenario = self.engine.generate_scenario_sync(
                {"name": research.get("title", "Topic"), "definition": ""},
                target_duration,
                scene_count
            )
            
            # Enhance scenario with research context
            if scenario.get("scenes"):
                scenario = self._enhance_scenario(scenario, research)
            
            scenario["success"] = True
            return scenario
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "scenes": []
            }
    
    def _build_scenario_prompt(
        self,
        research: Dict[str, Any],
        duration: int,
        custom_instructions: Optional[str]
    ) -> str:
        """Build detailed prompt for scenario generation."""
        concepts = research.get("concepts", [])
        formulas = research.get("formulas", [])
        
        concept_list = "\n".join([
            f"- {c.get('name', 'Unknown')}: {c.get('definition', '')}"
            for c in concepts[:5]  # Limit to top 5 concepts
        ])
        
        formula_list = "\n".join([
            f"- {f.get('latex', '')}: {f.get('explanation', '')}"
            for f in formulas[:3]  # Limit to top 3 formulas
        ])
        
        prompt = f"""
Create a detailed visualization scenario for educational content.

Topic: {research.get('title', 'Educational Topic')}
Duration: {duration} seconds
Level: {research.get('level', 'mixed')}

Key Concepts to Cover:
{concept_list}

Important Formulas:
{formula_list}

Requirements:
1. Create 4-6 scenes that progressively build understanding
2. Start with simple introduction, build to complex concepts
3. Each scene should have clear visual elements
4. Suggest appropriate visualization type (manim/matplotlib/plotly)
5. Include teaching points for each scene
6. Ensure smooth transitions between scenes

{f'Additional Instructions: {custom_instructions}' if custom_instructions else ''}

Generate a comprehensive scenario with detailed scene descriptions.
"""
        return prompt
    
    def _enhance_scenario(
        self,
        scenario: Dict[str, Any],
        research: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance generated scenario with research context."""
        scenes = scenario.get("scenes", [])
        concepts = research.get("concepts", [])
        formulas = research.get("formulas", [])
        
        # Add research references to scenes
        for i, scene in enumerate(scenes):
            # Add relevant concept if available
            if i < len(concepts):
                scene["related_concept"] = concepts[i].get("name", "")
            
            # Add relevant formula if available
            if i < len(formulas):
                scene["related_formula"] = formulas[i].get("latex", "")
        
        scenario["research_title"] = research.get("title", "")
        scenario["enhanced"] = True
        
        return scenario
    
    def validate_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate scenario structure and content.
        
        Args:
            scenario: Scenario data to validate
            
        Returns:
            Dict with validation results
        """
        validation = {
            "valid": True,
            "warnings": [],
            "errors": []
        }
        
        # Check for scenes
        if "scenes" not in scenario or not scenario["scenes"]:
            validation["valid"] = False
            validation["errors"].append("No scenes found in scenario")
            return validation
        
        scenes = scenario["scenes"]
        
        # Validate each scene
        required_scene_fields = ["title", "duration", "visualization_type"]
        
        for i, scene in enumerate(scenes, 1):
            # Check required fields
            for field in required_scene_fields:
                if field not in scene:
                    validation["warnings"].append(
                        f"Scene {i} missing field: {field}"
                    )
            
            # Validate visualization type
            valid_types = ["manim", "matplotlib", "plotly"]
            viz_type = scene.get("visualization_type", "").lower()
            if viz_type and viz_type not in valid_types:
                validation["warnings"].append(
                    f"Scene {i} has invalid visualization type: {viz_type}"
                )
            
            # Check duration
            duration = scene.get("duration", 0)
            if duration <= 0:
                validation["warnings"].append(
                    f"Scene {i} has invalid duration: {duration}"
                )
        
        # Check total duration
        total_duration = sum(s.get("duration", 0) for s in scenes)
        target_duration = scenario.get("total_duration", 0)
        
        if target_duration > 0:
            diff = abs(total_duration - target_duration)
            if diff > 30:  # More than 30 seconds difference
                validation["warnings"].append(
                    f"Total scene duration ({total_duration}s) differs significantly "
                    f"from target ({target_duration}s)"
                )
        
        return validation
    
    def suggest_visualization_type(
        self,
        scene_description: str,
        concept_type: str = "general"
    ) -> str:
        """
        Suggest appropriate visualization type based on content.
        
        Args:
            scene_description: Description of the scene
            concept_type: Type of concept (formula, graph, 3d, etc.)
            
        Returns:
            str: Suggested visualization type
        """
        description_lower = scene_description.lower()
        
        # Manim for mathematical animations
        manim_keywords = [
            "equation", "formula", "transformation", "proof",
            "geometric", "algebra", "calculus", "derivative"
        ]
        if any(kw in description_lower for kw in manim_keywords):
            return "manim"
        
        # Plotly for 3D and interactive
        plotly_keywords = [
            "3d", "three-dimensional", "surface", "vector field",
            "interactive", "rotation", "perspective"
        ]
        if any(kw in description_lower for kw in plotly_keywords):
            return "plotly"
        
        # Matplotlib for graphs and plots
        matplotlib_keywords = [
            "graph", "plot", "chart", "data", "function",
            "curve", "line", "scatter", "histogram"
        ]
        if any(kw in description_lower for kw in matplotlib_keywords):
            return "matplotlib"
        
        # Default based on concept type
        if concept_type in ["formula", "equation"]:
            return "manim"
        elif concept_type in ["3d", "spatial"]:
            return "plotly"
        else:
            return "matplotlib"
    
    def estimate_scene_duration(
        self,
        scene: Dict[str, Any],
        words_per_minute: int = 150
    ) -> int:
        """
        Estimate appropriate duration for a scene.
        
        Args:
            scene: Scene data
            words_per_minute: Speaking rate
            
        Returns:
            int: Estimated duration in seconds
        """
        # Base duration on script hint if available
        script_hint = scene.get("script_hint", "")
        if script_hint:
            word_count = len(script_hint.split())
            duration = int((word_count / words_per_minute) * 60)
            # Add buffer for visualization
            duration = int(duration * 1.5)
            return max(20, min(duration, 120))  # Between 20s and 2min
        
        # Default durations based on complexity
        teaching_points = scene.get("teaching_points", [])
        visual_elements = scene.get("visual_elements", [])
        
        base_duration = 30
        base_duration += len(teaching_points) * 10
        base_duration += len(visual_elements) * 5
        
        return min(base_duration, 90)  # Cap at 90 seconds


# Made with Bob