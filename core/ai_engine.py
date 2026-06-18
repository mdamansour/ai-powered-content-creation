"""
AI Engine for content generation using Google Gemini and other providers.
"""
import google.generativeai as genai
from typing import Dict, List, Optional, Any, Tuple
import json
import asyncio
from config.api_keys import APIConfig
from config.settings import get_settings


class GeminiModelRegistry:
    """Registry of available Gemini models with their capabilities."""
    
    # Task recommendations based on model naming patterns
    TASK_RECOMMENDATIONS = {
        "research": ["flash", "pro"],
        "scenario": ["pro", "flash"],
        "scripts": ["flash", "pro"],
        "quick_tasks": ["flash"],
        "complex_analysis": ["pro"],
        "detailed_content": ["pro", "flash"]
    }
    
    @classmethod
    def get_available_models(cls, api_key: str) -> List[Dict[str, Any]]:
        """
        Get list of available models dynamically from Google's API.
        
        Args:
            api_key: Gemini API key
            
        Returns:
            List of available model information
        """
        try:
            genai.configure(api_key=api_key)
            
            # Fetch models from Google's API
            models_list = genai.list_models()
            
            available = []
            for model in models_list:
                # Only include generative models (not embedding models, etc.)
                if 'generateContent' in model.supported_generation_methods:
                    model_info = cls._parse_model_info(model)
                    available.append(model_info)
            
            # Sort by name for consistent ordering
            available.sort(key=lambda x: x['id'])
            
            return available
            
        except Exception as e:
            print(f"Error fetching available models from API: {e}")
            # Return empty list if API call fails
            return []
    
    @classmethod
    def _parse_model_info(cls, model) -> Dict[str, Any]:
        """
        Parse model information from Google's API response.
        
        Args:
            model: Model object from genai.list_models()
            
        Returns:
            Dict with parsed model information
        """
        model_id = model.name.replace('models/', '')
        
        # Determine model capabilities based on name
        is_flash = 'flash' in model_id.lower()
        is_pro = 'pro' in model_id.lower()
        is_vision = model.supported_generation_methods and 'generateContent' in model.supported_generation_methods
        
        # Determine best use cases based on model type
        best_for = []
        if is_flash:
            best_for = ["research", "scripts", "quick_tasks"]
            description = "Fast and efficient, best for quick responses"
        elif is_pro:
            best_for = ["scenario", "complex_analysis", "detailed_content"]
            description = "Most capable, best for complex reasoning"
        else:
            best_for = ["general"]
            description = "General purpose model"
        
        # Get token limits from model metadata
        input_token_limit = getattr(model, 'input_token_limit', 8192)
        output_token_limit = getattr(model, 'output_token_limit', 2048)
        
        return {
            "id": model_id,
            "name": model.display_name if hasattr(model, 'display_name') else model_id,
            "description": description,
            "input_token_limit": input_token_limit,
            "output_token_limit": output_token_limit,
            "max_tokens": input_token_limit,  # For backward compatibility
            "supports_vision": is_vision,
            "best_for": best_for,
            "supported_methods": model.supported_generation_methods
        }
    
    @classmethod
    def get_model_info(cls, model_id: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific model.
        
        Args:
            model_id: Model identifier
            api_key: Optional API key (uses configured key if not provided)
            
        Returns:
            Dict with model information or None
        """
        try:
            if api_key:
                genai.configure(api_key=api_key)
            
            # Fetch all models and find the matching one
            models = cls.get_available_models(api_key or "")
            for model in models:
                if model['id'] == model_id:
                    return model
            
            return None
        except Exception as e:
            print(f"Error getting model info: {e}")
            return None
    
    @classmethod
    def recommend_model(cls, task_type: str, api_key: Optional[str] = None) -> Optional[str]:
        """
        Recommend best model for a specific task.
        
        Args:
            task_type: Type of task ('research', 'scenario', 'script', etc.)
            api_key: Optional API key
            
        Returns:
            Recommended model ID or None
        """
        try:
            # Get available models
            models = cls.get_available_models(api_key or "")
            
            if not models:
                return None
            
            # Get task preferences
            preferences = cls.TASK_RECOMMENDATIONS.get(task_type, ["flash", "pro"])
            
            # Find best matching model
            for preference in preferences:
                for model in models:
                    if preference in model['id'].lower():
                        # Prefer "latest" versions
                        if 'latest' in model['id'].lower():
                            return model['id']
            
            # If no preference match, try any model with the task in best_for
            for model in models:
                if task_type in model.get('best_for', []):
                    return model['id']
            
            # Default to first available model
            return models[0]['id'] if models else None
            
        except Exception as e:
            print(f"Error recommending model: {e}")
            return None


class AIEngine:
    """Main AI engine for educational content generation."""
    
    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize AI engine.
        
        Args:
            provider: AI provider name ('gemini', 'openai', 'anthropic')
            api_key: API key (optional, will use from config if not provided)
            model: Specific model to use (optional, uses default from settings)
        """
        settings = get_settings()
        
        # Determine provider
        if provider is None:
            provider = settings.ai.provider
        self.provider = provider.lower() if provider else "gemini"
        
        # Get API key
        if api_key is None:
            api_key = APIConfig.get_api_key(self.provider)
        
        if not api_key:
            raise ValueError(f"No API key found for provider: {self.provider}")
        
        self.api_key = api_key
        self.settings = settings.ai
        self.current_model_id = model or self.settings.model
        
        # Initialize provider-specific client
        if self.provider == "gemini":
            genai.configure(api_key=self.api_key)
            self._initialize_gemini_model(self.current_model_id)
        else:
            raise NotImplementedError(f"Provider {self.provider} not yet implemented")
    
    def _initialize_gemini_model(self, model_id: str):
        """Initialize Gemini model with given ID."""
        self.model = genai.GenerativeModel(
            model_id,
            generation_config={
                "temperature": self.settings.temperature,
                "max_output_tokens": self.settings.max_tokens,
            }
        )
        self.chat = None
        self.current_model_id = model_id
    
    def switch_model(self, model_id: str) -> bool:
        """
        Switch to a different model.
        
        Args:
            model_id: ID of the model to switch to
            
        Returns:
            bool: True if successful
        """
        try:
            if self.provider == "gemini":
                self._initialize_gemini_model(model_id)
                return True
            else:
                raise NotImplementedError(f"Model switching not implemented for {self.provider}")
        except Exception as e:
            print(f"Error switching model: {e}")
            return False
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models for current provider.
        
        Returns:
            List of model information dictionaries
        """
        if self.provider == "gemini":
            return GeminiModelRegistry.get_available_models(self.api_key)
        else:
            return []
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """
        Get information about currently active model.
        
        Returns:
            Dict with model information
        """
        if self.provider == "gemini":
            info = GeminiModelRegistry.get_model_info(self.current_model_id)
            if info:
                return {
                    "id": self.current_model_id,
                    "provider": self.provider,
                    **info
                }
        
        return {
            "id": self.current_model_id,
            "provider": self.provider,
            "name": self.current_model_id
        }
    
    def recommend_model_for_task(self, task_type: str) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Get recommended model for a specific task.
        
        Args:
            task_type: Type of task ('research', 'scenario', 'script', etc.)
            
        Returns:
            Tuple of (model_id, model_info)
        """
        if self.provider == "gemini":
            model_id = GeminiModelRegistry.recommend_model(task_type, self.api_key)
            info = GeminiModelRegistry.get_model_info(model_id, self.api_key) if model_id else None
            return model_id, info
        
        return self.current_model_id, self.get_current_model_info()
    
    def start_session(self, system_prompt: Optional[str] = None):
        """
        Initialize a chat session with optional system context.
        
        Args:
            system_prompt: System-level instructions for the AI
        """
        if self.provider == "gemini":
            self.chat = self.model.start_chat(history=[])
            if system_prompt:
                # Send system prompt as first message
                self.chat.send_message(system_prompt)
        return self.chat
    
    async def generate_research(self, topic: str, level: str = "mixed") -> Dict[str, Any]:
        """
        Generate comprehensive research for an educational topic.
        
        Args:
            topic: The educational topic to research
            level: Educational level ('high_school', 'university', 'mixed')
            
        Returns:
            Dict containing structured research data
        """
        print(f"\n[AIEngine] Building prompt for topic: '{topic}'")
        prompt = self._build_research_prompt(topic, level)
        
        # Log first 500 chars of prompt to verify it's correct
        print(f"[AIEngine] Prompt preview (first 500 chars):")
        print(f"{prompt[:500]}...")
        print(f"[AIEngine] Sending request to {self.provider} model: {self.current_model_id}")
        
        try:
            response = await self._generate_async(prompt)
            
            # Log response preview
            print(f"\n[AIEngine] Raw AI response (first 500 chars):")
            print(f"{response[:500]}...")
            
            result = self._parse_json_response(response)
            
            print(f"[AIEngine] Parsed JSON successfully")
            print(f"[AIEngine] Title in response: '{result.get('title', 'N/A')}'")
            print(f"[AIEngine] Topic field in response: '{result.get('topic', 'N/A')}'")
            
            # Post-process: Force correct topic and remove unwanted fields
            if isinstance(result, dict) and result.get("parsed") != False:
                original_title = result.get("title")
                
                # Force the title to match the input topic
                result["title"] = topic
                
                if original_title != topic:
                    print(f"[AIEngine] ⚠️  Title mismatch! AI returned '{original_title}', forcing to '{topic}'")
                
                # Remove any "topic", "subject", or "category" fields the AI might have added
                removed_fields = []
                for field in ["topic", "subject", "category", "subject_area"]:
                    if field in result:
                        removed_fields.append(f"{field}='{result[field]}'")
                        result.pop(field)
                
                if removed_fields:
                    print(f"[AIEngine] ⚠️  Removed AI-added fields: {', '.join(removed_fields)}")
                
                # Ensure all concepts are relevant (basic validation)
                if "concepts" in result and isinstance(result["concepts"], list):
                    print(f"[AIEngine] Found {len(result['concepts'])} concepts")
                    if result["concepts"]:
                        print(f"[AIEngine] First concept: '{result['concepts'][0].get('name', 'N/A')}'")
            
            print(f"[AIEngine] Research generation complete\n")
            return result
        except Exception as e:
            print(f"[AIEngine] ERROR: {str(e)}\n")
            return {
                "error": str(e),
                "topic": topic,
                "level": level,
                "parsed": False
            }
    
    async def generate_scenario(self, concept: Dict[str, Any], duration: int = 300, scene_count: int = 5) -> Dict[str, Any]:
        """
        Generate visualization scenario for a concept.
        
        Args:
            concept: Dictionary containing concept information
            duration: Target duration in seconds
            scene_count: Desired number of scenes
            
        Returns:
            Dict containing scene-by-scene scenario
        """
        prompt = self._build_scenario_prompt(concept, duration, scene_count)
        
        try:
            response = await self._generate_async(prompt)
            return self._parse_json_response(response)
        except Exception as e:
            return {
                "error": str(e),
                "concept": concept.get("name", "Unknown"),
                "parsed": False
            }
    def generate_scenario_sync(self, concept: Dict[str, Any], duration: int = 300, scene_count: int = 5) -> Dict[str, Any]:
        """
        Generate visualization scenario for a concept (synchronous version).
        
        Args:
            concept: Dictionary containing concept information
            duration: Target duration in seconds
            scene_count: Desired number of scenes
            
        Returns:
            Dict containing scene-by-scene scenario
        """
        prompt = self._build_scenario_prompt(concept, duration, scene_count)
        
        try:
            response = self.generate(prompt)
            return self._parse_json_response(response)
        except Exception as e:
            return {
                "error": str(e),
                "concept": concept.get("name", "Unknown"),
                "parsed": False
            }
    
    def generate_script_sync(self, scene: Dict[str, Any]) -> str:
        """
        Generate narration script for a scene (synchronous version).
        
        Args:
            scene: Dictionary containing scene information
            
        Returns:
            str: Generated script text
        """
        prompt = self._build_script_prompt(scene)
        
        try:
            response = self.generate(prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    
    async def generate_script(self, scene: Dict[str, Any]) -> str:
        """
        Generate narration script for a scene.
        
        Args:
            scene: Dictionary containing scene information
            
        Returns:
            str: Generated script text
        """
        prompt = self._build_script_prompt(scene)
        
        try:
            response = await self._generate_async(prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    async def _generate_async(self, prompt: str) -> str:
        """
        Generate content asynchronously.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            str: Generated text response
        """
        if self.provider == "gemini":
            response = await self.model.generate_content_async(prompt)
            return response.text
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
    
    def generate(self, prompt: str) -> str:
        """
        Generate content synchronously.
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            str: Generated text response
        """
        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            return response.text
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented")
    
    def _build_research_prompt(self, topic: str, level: str) -> str:
        """Build prompt for research generation."""
        import time
        import random
        
        # Add unique timestamp and random number to prevent caching
        unique_id = f"{int(time.time())}-{random.randint(1000, 9999)}"
        
        return f"""
[REQUEST_ID: {unique_id}]

You are an expert educator specializing in mathematics and physics.

CRITICAL INSTRUCTION: You MUST research ONLY the EXACT topic provided. DO NOT generalize or broaden the topic.

EXACT TOPIC TO RESEARCH: "{topic}"
Educational Level: {level}

IMPORTANT EXAMPLES:
✅ CORRECT: If topic is "Even and Odd numbers" → Research ONLY even/odd numbers (divisibility by 2, properties like 2k and 2k+1, parity rules)
✅ CORRECT: If topic is "Projectile Motion" → Research ONLY projectile motion (trajectory, range, time of flight)
✅ CORRECT: If topic is "Quadratic Equations" → Research ONLY quadratic equations (ax²+bx+c=0, quadratic formula)

❌ WRONG: If topic is "Even and Odd numbers" → DO NOT research "Algebra", "Number Theory", or "Variables"
❌ WRONG: If topic is "Projectile Motion" → DO NOT research "Mechanics", "Newton's Laws", or general "Physics"
❌ WRONG: If topic is "Quadratic Equations" → DO NOT research "Polynomials", "Functions", or general "Algebra"

YOUR TASK: Research the EXACT topic "{topic}" - nothing broader, nothing different.

For the topic "{topic}", provide:

1. **Core Concepts**: Concepts DIRECTLY about "{topic}"
2. **Mathematical Formulas**: Formulas used IN "{topic}"
3. **Physical Principles**: Principles OF "{topic}"
4. **Prerequisites**: What students need BEFORE learning "{topic}"
5. **Real-World Applications**: Where "{topic}" is USED
6. **Common Misconceptions**: Errors students make WITH "{topic}"
7. **Practice Problems**: Problems TO PRACTICE "{topic}"

STRICT JSON REQUIREMENTS:
- "title" MUST be: "{topic}" (exact match)
- DO NOT include "topic", "subject", "category", or "subject_area" fields
- Every concept name must relate to "{topic}"
- Every formula must be used in "{topic}"

Return this JSON structure ONLY:
{{
  "title": "{topic}",
  "concepts": [
    {{
      "name": "Concept name (must relate to {topic})",
      "definition": "Definition",
      "importance": "Why it matters for {topic}"
    }}
  ],
  "formulas": [
    {{
      "latex": "Formula used in {topic}",
      "explanation": "What it means in context of {topic}",
      "variables": {{"var": "description"}}
    }}
  ],
  "principles": ["Principle of {topic}"],
  "prerequisites": ["What's needed before {topic}"],
  "applications": ["Where {topic} is used"],
  "misconceptions": ["Common errors with {topic}"],
  "practice_problems": ["Problem for {topic}"]
}}

VERIFICATION CHECKLIST:
□ Title is exactly "{topic}"
□ All concepts are about "{topic}"
□ All formulas are used in "{topic}"
□ No "topic" or "subject" fields added
□ Content is NOT about a broader subject

Return ONLY valid JSON. No markdown, no explanations, just JSON.
"""
    
    def _build_scenario_prompt(self, concept: Dict[str, Any], duration: int, scene_count: int = 5) -> str:
        """Build prompt for scenario generation with 3Blue1Brown-quality Manim code."""
        concept_name = concept.get("name", "Unknown")
        concept_def = concept.get("definition", "")
        
        # Calculate average duration per scene
        avg_duration = duration // scene_count
        
        return f"""
You are an EXPERT Manim animator creating 3Blue1Brown-quality educational content.

Concept: {concept_name}
Definition: {concept_def}
Target Duration: {duration} seconds
Required Scenes: {scene_count}

CRITICAL: Generate PROFESSIONAL, 3BLUE1BROWN-STYLE Manim code for EACH scene.

=== 3BLUE1BROWN QUALITY STANDARDS ===

1. VISUAL STORYTELLING
   - Progressive concept building (simple → complex)
   - Smooth equation transformations using Transform()
   - Geometric constructions with annotations
   - Visual metaphors for abstract concepts

2. ADVANCED MANIM FEATURES (MUST USE)
   - MathTex() for equations with LaTeX
   - NumberPlane/Axes for coordinate systems
   - Vector/Arrow for directional concepts
   - Dot with labels for points
   - Graph() for function plotting
   - Brace/DoubleArrow for annotations
   - SurroundingRectangle for emphasis
   - VGroup for grouping elements

3. PROFESSIONAL COLOR SCHEME (3Blue1Brown palette)
   - Background: "#0C0C0C" (near black)
   - Primary: "#58C4DD" (signature blue)
   - Secondary: "#83C167" (green)
   - Accent: "#FC6255" (red/pink)
   - Text: "#ECECEC" (light gray)
   - Highlight: "#FFFF00" (yellow)

4. SMOOTH ANIMATIONS
   - Use rate_func=smooth for natural motion
   - Transform() for equation morphing
   - Create() for drawing shapes
   - Write() for text/equations
   - GrowArrow() for vectors
   - FadeIn/FadeOut with proper timing

5. VISUAL HIERARCHY
   - Title: 48pt, bold, top edge
   - Equations: 40pt, centered
   - Body text: 32pt
   - Labels: 24pt
   - Proper spacing and alignment

=== EXAMPLE: EQUATION TRANSFORMATION ===
```python
# Show general quadratic
eq1 = MathTex("ax^2 + bx + c = 0", color="#ECECEC")
eq1.scale(1.2)
self.play(Write(eq1), run_time=1.5)
self.wait(0.5)

# Transform to specific example
eq2 = MathTex("x^2 + 5x + 6 = 0", color="#58C4DD")
eq2.scale(1.2)
self.play(Transform(eq1, eq2), run_time=1.5)
self.wait(0.5)

# Factor it
eq3 = MathTex("(x + 2)(x + 3) = 0", color="#83C167")
eq3.scale(1.2)
self.play(Transform(eq1, eq3), run_time=1.5)
self.wait(1)
```

=== EXAMPLE: GEOMETRIC CONSTRUCTION ===
```python
# Create axes
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 8, 2],
    axis_config={{"color": "#404040"}},
    tips=True
)
labels = axes.get_axis_labels(x_label="x", y_label="y")
self.play(Create(axes), Write(labels), run_time=2)

# Plot function
graph = axes.plot(lambda x: x**2, color="#58C4DD", stroke_width=4)
func_label = MathTex("f(x) = x^2", color="#58C4DD").to_edge(UP)
self.play(Create(graph), Write(func_label), run_time=2)

# Highlight point
point = Dot(axes.c2p(2, 4), color="#FC6255", radius=0.1)
coords = MathTex("(2, 4)", color="#FC6255").next_to(point, UR)
self.play(GrowFromCenter(point), Write(coords), run_time=1)
```

=== EXAMPLE: VECTOR VISUALIZATION ===
```python
# Number plane
plane = NumberPlane(
    background_line_style={{
        "stroke_color": "#404040",
        "stroke_width": 1,
        "stroke_opacity": 0.3
    }}
)
self.play(Create(plane), run_time=1.5)

# Create vectors
v1 = Vector([2, 1], color="#58C4DD", stroke_width=4)
v2 = Vector([1, 2], color="#83C167", stroke_width=4)
v1_label = MathTex("\\\\vec{{v}}_1", color="#58C4DD").next_to(v1.get_end(), RIGHT)
v2_label = MathTex("\\\\vec{{v}}_2", color="#83C167").next_to(v2.get_end(), UP)

self.play(GrowArrow(v1), Write(v1_label), run_time=1)
self.play(GrowArrow(v2), Write(v2_label), run_time=1)

# Show sum
v_sum = Vector([3, 3], color="#FC6255", stroke_width=5)
sum_label = MathTex("\\\\vec{{v}}_1 + \\\\vec{{v}}_2", color="#FC6255").next_to(v_sum.get_end(), UR)
self.play(GrowArrow(v_sum), Write(sum_label), run_time=1.5)
```

=== JSON FORMAT ===
Return EXACTLY {scene_count} scenes with this structure:
{{
  "total_duration": {duration},
  "scenes": [
    {{
      "id": 1,
      "title": "Introduction: {concept_name}",
      "duration": {avg_duration},
      "visualization_type": "manim",
      "manim_code": "# COMPLETE, EXECUTABLE CODE HERE\\n# Use MathTex, Transform, Create, etc.\\n# Include colors from 3B1B palette\\n# Smooth animations with proper timing",
      "visual_elements": ["Equation transformation", "Geometric diagram", "Annotations"],
      "animation_description": "Detailed description of visual flow",
      "teaching_points": ["Key concept 1", "Key concept 2"],
      "transition": "Smooth fade to next scene"
    }},
    ... (continue for all {scene_count} scenes)
  ]
}}

=== CRITICAL REQUIREMENTS ===
✓ EXACTLY {scene_count} scenes
✓ Each scene has COMPLETE, WORKING Manim code
✓ Use MathTex for ALL equations
✓ Use 3Blue1Brown color palette
✓ Include geometric diagrams where relevant
✓ Smooth Transform() animations
✓ Professional visual hierarchy
✓ Progressive complexity building
✓ Proper timing (1-2s per animation)
✓ Clear annotations and labels
✓ Total duration = {duration} seconds

Return ONLY valid JSON with professional Manim code.
"""
    
    def _build_script_prompt(self, scene: Dict[str, Any]) -> str:
        """Build prompt for script generation."""
        title = scene.get("title", "Untitled")
        duration = scene.get("duration", 30)
        visual_elements = scene.get("visual_elements", [])
        teaching_points = scene.get("teaching_points", [])
        
        # Calculate target word count (assuming ~150 words per minute)
        target_words = int((duration / 60) * 150)
        
        return f"""
You are a skilled educational content writer.

Scene: {title}
Duration: {duration} seconds
Visual Elements: {', '.join(visual_elements)}
Key Teaching Points: {', '.join(teaching_points)}

Write engaging narration that:
- Explains the concept clearly and conversationally
- Matches the {duration}-second timing
- References the visual elements naturally
- Covers all teaching points
- Uses simple, accessible language
- Includes rhetorical questions for engagement
- Provides smooth transitions

Target word count: approximately {target_words} words
(Based on ~150 words per minute speaking rate)

Return ONLY the script text, no additional formatting or explanations.
"""
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        Parse JSON from AI response, handling markdown code blocks.
        
        Args:
            text: Raw text response from AI
            
        Returns:
            Dict: Parsed JSON data
        """
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            # Fallback: return raw text with error flag
            return {
                "raw_text": text,
                "parsed": False,
                "error": f"JSON parsing error: {str(e)}"
            }
    
    def validate_response(self, response: Dict[str, Any], required_keys: List[str]) -> bool:
        """
        Validate that response contains required keys.
        
        Args:
            response: Response dictionary to validate
            required_keys: List of required key names
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not isinstance(response, dict):
            return False
        
        if response.get("parsed") is False:
            return False
        
        return all(key in response for key in required_keys)

# Made with Bob
