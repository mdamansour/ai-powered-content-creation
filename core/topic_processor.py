"""
Topic processing and research generation for educational content.
"""
import asyncio
from typing import Dict, List, Optional, Any
from core.ai_engine import AIEngine
from utils.model_selector import ModelSelector


class TopicProcessor:
    """Process educational topics and generate research."""
    
    # Predefined topic categories
    MATH_TOPICS = [
        "Algebra",
        "Calculus",
        "Geometry",
        "Trigonometry",
        "Linear Algebra",
        "Differential Equations",
        "Statistics",
        "Probability",
        "Number Theory",
        "Complex Numbers"
    ]
    
    PHYSICS_TOPICS = [
        "Classical Mechanics",
        "Electromagnetism",
        "Thermodynamics",
        "Quantum Mechanics",
        "Optics",
        "Waves and Oscillations",
        "Relativity",
        "Fluid Dynamics",
        "Nuclear Physics",
        "Particle Physics"
    ]
    
    @classmethod
    def get_all_topics(cls) -> Dict[str, List[str]]:
        """Get all predefined topics organized by category."""
        return {
            "Mathematics": cls.MATH_TOPICS,
            "Physics": cls.PHYSICS_TOPICS
        }
    
    @classmethod
    def get_topic_suggestions(cls, query: str) -> List[str]:
        """
        Get topic suggestions based on search query.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching topics
        """
        query_lower = query.lower()
        suggestions = []
        
        all_topics = cls.MATH_TOPICS + cls.PHYSICS_TOPICS
        for topic in all_topics:
            if query_lower in topic.lower():
                suggestions.append(topic)
        
        return suggestions
    
    def __init__(self, engine: Optional[AIEngine] = None):
        """
        Initialize topic processor.
        
        Args:
            engine: Optional AI engine (creates one if not provided)
        """
        self.engine = engine or ModelSelector.get_engine_for_task("research")
    
    async def generate_research(
        self,
        topic: str,
        level: str = "mixed",
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive research for a topic.
        
        Args:
            topic: Educational topic to research
            level: Educational level ('high_school', 'university', 'mixed')
            custom_instructions: Optional additional instructions
            
        Returns:
            Dict containing research data
        """
        try:
            print(f"\n{'='*60}")
            print(f"[TopicProcessor] Generating research for: '{topic}'")
            print(f"[TopicProcessor] Level: {level}")
            print(f"{'='*60}\n")
            
            # Generate research using AI
            research = await self.engine.generate_research(topic, level)
            
            # DEBUG: Log what AI returned
            print(f"\n[TopicProcessor] AI Response received:")
            print(f"  - Title from AI: {research.get('title', 'N/A')}")
            print(f"  - Topic field from AI: {research.get('topic', 'N/A')}")
            print(f"  - Success: {research.get('success', 'N/A')}")
            print(f"  - Parsed: {research.get('parsed', 'N/A')}")
            
            # CRITICAL: Remove any topic/subject fields the AI added
            # These are wrong and should not be in the response
            ai_added_topic = research.pop("topic", None)
            ai_added_subject = research.pop("subject", None)
            ai_added_category = research.pop("category", None)
            
            if ai_added_topic:
                print(f"  ⚠️  WARNING: AI added 'topic' field: '{ai_added_topic}' (REMOVED)")
            if ai_added_subject:
                print(f"  ⚠️  WARNING: AI added 'subject' field: '{ai_added_subject}' (REMOVED)")
            if ai_added_category:
                print(f"  ⚠️  WARNING: AI added 'category' field: '{ai_added_category}' (REMOVED)")
            
            # Add correct metadata
            research["topic"] = topic  # Use the INPUT topic, not AI's categorization
            research["level"] = level
            research["success"] = research.get("parsed", True) != False
            
            print(f"\n[TopicProcessor] Final research data:")
            print(f"  - Title (corrected): {research.get('title')}")
            print(f"  - Topic (forced): {research.get('topic')}")
            print(f"  - Number of concepts: {len(research.get('concepts', []))}")
            print(f"{'='*60}\n")
            
            if custom_instructions:
                research["custom_instructions"] = custom_instructions
            
            return research
            
        except Exception as e:
            print(f"\n[TopicProcessor] ERROR: {str(e)}\n")
            return {
                "topic": topic,
                "level": level,
                "success": False,
                "error": str(e),
                "parsed": False
            }
    
    def validate_research(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate research data structure.
        
        Args:
            research: Research data to validate
            
        Returns:
            Dict with validation results
        """
        required_keys = ["title", "concepts", "formulas", "principles"]
        
        validation = {
            "valid": True,
            "missing_keys": [],
            "warnings": []
        }
        
        # Check required keys
        for key in required_keys:
            if key not in research:
                validation["valid"] = False
                validation["missing_keys"].append(key)
        
        # Check if parsed successfully
        if research.get("parsed") is False:
            validation["valid"] = False
            validation["warnings"].append("JSON parsing failed")
        
        # Check for errors
        if "error" in research:
            validation["valid"] = False
            validation["warnings"].append(f"Error: {research['error']}")
        
        # Validate concepts structure
        if "concepts" in research:
            if not isinstance(research["concepts"], list):
                validation["warnings"].append("Concepts should be a list")
            elif len(research["concepts"]) == 0:
                validation["warnings"].append("No concepts found")
        
        # Validate formulas structure
        if "formulas" in research:
            if not isinstance(research["formulas"], list):
                validation["warnings"].append("Formulas should be a list")
        
        return validation
    
    def extract_key_concepts(self, research: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Extract key concepts from research data.
        
        Args:
            research: Research data
            
        Returns:
            List of concept dictionaries
        """
        concepts = research.get("concepts", [])
        
        if not isinstance(concepts, list):
            return []
        
        # Ensure each concept has required fields
        formatted_concepts = []
        for concept in concepts:
            if isinstance(concept, dict):
                formatted_concepts.append({
                    "name": concept.get("name", "Unnamed Concept"),
                    "definition": concept.get("definition", ""),
                    "importance": concept.get("importance", "")
                })
            elif isinstance(concept, str):
                # Handle simple string concepts
                formatted_concepts.append({
                    "name": concept,
                    "definition": "",
                    "importance": ""
                })
        
        return formatted_concepts
    
    def extract_formulas(self, research: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract formulas from research data.
        
        Args:
            research: Research data
            
        Returns:
            List of formula dictionaries
        """
        formulas = research.get("formulas", [])
        
        if not isinstance(formulas, list):
            return []
        
        # Ensure each formula has required fields
        formatted_formulas = []
        for formula in formulas:
            if isinstance(formula, dict):
                formatted_formulas.append({
                    "latex": formula.get("latex", ""),
                    "explanation": formula.get("explanation", ""),
                    "variables": formula.get("variables", {})
                })
        
        return formatted_formulas
    
    def enrich_research(
        self,
        research: Dict[str, Any],
        user_notes: Optional[str] = None,
        additional_concepts: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Enrich research with user input.
        
        Args:
            research: Original research data
            user_notes: Optional user notes
            additional_concepts: Optional additional concepts to add
            
        Returns:
            Enriched research data
        """
        enriched = research.copy()
        
        if user_notes:
            enriched["user_notes"] = user_notes
        
        if additional_concepts:
            current_concepts = enriched.get("concepts", [])
            enriched["concepts"] = current_concepts + additional_concepts
        
        enriched["enriched"] = True
        
        return enriched


# Made with Bob