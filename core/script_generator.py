"""
Script generation for creating narration synchronized with visualization scenes.
"""
import asyncio
from typing import Dict, List, Optional, Any
from core.ai_engine import AIEngine
from utils.model_selector import ModelSelector


class ScriptGenerator:
    """Generate narration scripts for visualization scenes."""
    
    def __init__(self, engine: Optional[AIEngine] = None):
        """
        Initialize script generator.
        
        Args:
            engine: Optional AI engine (creates one if not provided)
        """
        self.engine = engine or ModelSelector.get_engine_for_task("scripts")
    
    async def generate_script(
        self,
        scene: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate narration script for a scene.
        
        Args:
            scene: Scene data dictionary
            context: Optional context (previous scenes, research data, etc.)
            
        Returns:
            str: Generated script text
        """
        try:
            # Generate script using AI
            script = await self.engine.generate_script(scene)
            
            # Post-process script
            script = self._post_process_script(script, scene)
            
            return script
            
        except Exception as e:
            return f"Error generating script: {str(e)}"
    
    async def generate_all_scripts(
        self,
        scenes: List[Dict[str, Any]],
        research: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Generate scripts for all scenes.
        
        Args:
            scenes: List of scene dictionaries
            research: Optional research data for context
            
        Returns:
            Dict mapping scene IDs to scripts
        """
        scripts = {}
        
        for i, scene in enumerate(scenes):
            # Build context from previous scenes
            context = {
                "scene_number": i + 1,
                "total_scenes": len(scenes),
                "previous_scenes": scenes[:i] if i > 0 else [],
                "research": research
            }
            
            # Generate script
            script = await self.generate_script(scene, context)
            
            # Store with scene ID
            scene_id = scene.get("id", i + 1)
            scripts[str(scene_id)] = script
        
        return scripts
    
    def _post_process_script(
        self,
        script: str,
        scene: Dict[str, Any]
    ) -> str:
        """
        Post-process generated script.
        
        Args:
            script: Raw generated script
            scene: Scene data
            
        Returns:
            str: Processed script
        """
        # Remove any markdown formatting
        script = script.replace("**", "")
        script = script.replace("*", "")
        
        # Remove code blocks if present
        if "```" in script:
            lines = script.split("\n")
            script = "\n".join([
                line for line in lines
                if not line.strip().startswith("```")
            ])
        
        # Ensure proper spacing
        script = script.strip()
        
        # Add scene markers if needed
        scene_title = scene.get("title", "")
        if scene_title and not script.startswith(scene_title):
            script = f"[{scene_title}]\n\n{script}"
        
        return script
    
    def estimate_word_count(
        self,
        duration: int,
        words_per_minute: int = 150
    ) -> int:
        """
        Estimate target word count for a given duration.
        
        Args:
            duration: Duration in seconds
            words_per_minute: Speaking rate
            
        Returns:
            int: Target word count
        """
        minutes = duration / 60
        return int(minutes * words_per_minute)
    
    def calculate_duration(
        self,
        script: str,
        words_per_minute: int = 150
    ) -> int:
        """
        Calculate estimated duration for a script.
        
        Args:
            script: Script text
            words_per_minute: Speaking rate
            
        Returns:
            int: Estimated duration in seconds
        """
        word_count = len(script.split())
        minutes = word_count / words_per_minute
        return int(minutes * 60)
    
    def validate_script(
        self,
        script: str,
        scene: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate script against scene requirements.
        
        Args:
            script: Script text
            scene: Scene data
            
        Returns:
            Dict with validation results
        """
        validation = {
            "valid": True,
            "warnings": [],
            "word_count": len(script.split()),
            "estimated_duration": self.calculate_duration(script)
        }
        
        # Check if script is empty
        if not script or len(script.strip()) < 10:
            validation["valid"] = False
            validation["warnings"].append("Script is too short or empty")
            return validation
        
        # Check duration match
        target_duration = scene.get("duration", 0)
        if target_duration > 0:
            estimated = validation["estimated_duration"]
            diff = abs(estimated - target_duration)
            
            if diff > 10:  # More than 10 seconds difference
                validation["warnings"].append(
                    f"Script duration ({estimated}s) differs from target ({target_duration}s)"
                )
        
        # Check for teaching points coverage
        teaching_points = scene.get("teaching_points", [])
        if teaching_points:
            script_lower = script.lower()
            missing_points = []
            
            for point in teaching_points:
                # Simple keyword check
                keywords = point.lower().split()[:3]  # First 3 words
                if not any(kw in script_lower for kw in keywords):
                    missing_points.append(point)
            
            if missing_points:
                validation["warnings"].append(
                    f"May not cover all teaching points: {', '.join(missing_points[:2])}"
                )
        
        return validation
    
    def add_emphasis_markers(
        self,
        script: str,
        keywords: List[str]
    ) -> str:
        """
        Add emphasis markers to script for important keywords.
        
        Args:
            script: Script text
            keywords: List of keywords to emphasize
            
        Returns:
            str: Script with emphasis markers
        """
        for keyword in keywords:
            # Add emphasis markers (can be used by TTS or for highlighting)
            script = script.replace(
                keyword,
                f"*{keyword}*"
            )
        
        return script
    
    def split_into_segments(
        self,
        script: str,
        max_segment_duration: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Split script into smaller segments for recording.
        
        Args:
            script: Full script text
            max_segment_duration: Maximum duration per segment in seconds
            
        Returns:
            List of segment dictionaries
        """
        # Split by sentences
        sentences = script.replace("! ", "!|").replace("? ", "?|").replace(". ", ".|").split("|")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        segments = []
        current_segment = []
        current_duration = 0
        
        for sentence in sentences:
            sentence_duration = self.calculate_duration(sentence)
            
            if current_duration + sentence_duration > max_segment_duration and current_segment:
                # Save current segment
                segment_text = " ".join(current_segment)
                segments.append({
                    "text": segment_text,
                    "duration": current_duration,
                    "sentence_count": len(current_segment)
                })
                
                # Start new segment
                current_segment = [sentence]
                current_duration = sentence_duration
            else:
                current_segment.append(sentence)
                current_duration += sentence_duration
        
        # Add final segment
        if current_segment:
            segment_text = " ".join(current_segment)
            segments.append({
                "text": segment_text,
                "duration": current_duration,
                "sentence_count": len(current_segment)
            })
        
        return segments
    
    def generate_timing_markers(
        self,
        script: str,
        scene_duration: int
    ) -> List[Dict[str, Any]]:
        """
        Generate timing markers for script synchronization.
        
        Args:
            script: Script text
            scene_duration: Total scene duration in seconds
            
        Returns:
            List of timing markers
        """
        sentences = script.replace("! ", "!|").replace("? ", "?|").replace(". ", ".|").split("|")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        markers = []
        current_time = 0
        
        for i, sentence in enumerate(sentences):
            sentence_duration = self.calculate_duration(sentence)
            
            markers.append({
                "index": i,
                "text": sentence,
                "start_time": current_time,
                "end_time": current_time + sentence_duration,
                "duration": sentence_duration
            })
            
            current_time += sentence_duration
        
        # Normalize to fit scene duration
        if current_time > 0:
            scale_factor = scene_duration / current_time
            for marker in markers:
                marker["start_time"] = int(marker["start_time"] * scale_factor)
                marker["end_time"] = int(marker["end_time"] * scale_factor)
                marker["duration"] = marker["end_time"] - marker["start_time"]
        
        return markers


# Made with Bob