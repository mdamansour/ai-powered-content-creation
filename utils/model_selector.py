"""
Utility for convenient model selection and AI engine creation.
"""
from typing import Optional, Dict, Any
from core.ai_engine import AIEngine, GeminiModelRegistry
from config.api_keys import APIConfig


class ModelSelector:
    """Helper class for model selection and engine creation."""
    
    @staticmethod
    def get_engine_for_task(
        task_type: str,
        custom_model: Optional[str] = None,
        provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> AIEngine:
        """
        Get an AI engine configured for a specific task.
        
        Args:
            task_type: Type of task ('research', 'scenario', 'scripts', etc.)
            custom_model: Optional specific model to use
            provider: Optional AI provider (defaults to configured)
            api_key: Optional API key (defaults to configured)
            
        Returns:
            AIEngine: Configured AI engine instance
        """
        # Determine provider
        if provider is None:
            provider = APIConfig.get_active_provider() or "gemini"
        
        # Get API key
        if api_key is None:
            api_key = APIConfig.get_api_key(provider)
        
        # Determine model
        if custom_model:
            model = custom_model
        else:
            # Get recommended model for task
            if provider == "gemini":
                model = GeminiModelRegistry.recommend_model(task_type, api_key)
            else:
                model = None  # Use provider default
        
        # Create and return engine
        return AIEngine(provider=provider, api_key=api_key, model=model)
    
    @staticmethod
    def recommend_model(task_type: str, provider: str = "gemini") -> Optional[str]:
        """
        Get recommended model for a task.
        
        Args:
            task_type: Type of task
            provider: AI provider
            
        Returns:
            str: Recommended model ID or None
        """
        if provider == "gemini":
            api_key = APIConfig.get_api_key("gemini")
            return GeminiModelRegistry.recommend_model(task_type, api_key)
        return None
    
    @staticmethod
    def get_available_models(provider: str = "gemini") -> list:
        """
        Get list of available models for provider.
        
        Args:
            provider: AI provider
            
        Returns:
            list: Available models
        """
        if provider == "gemini":
            api_key = APIConfig.get_api_key("gemini")
            if api_key:
                return GeminiModelRegistry.get_available_models(api_key)
        return []
    
    @staticmethod
    def get_model_info(model_id: str, provider: str = "gemini") -> Optional[Dict[str, Any]]:
        """
        Get information about a specific model.
        
        Args:
            model_id: Model identifier
            provider: AI provider
            
        Returns:
            Dict: Model information or None
        """
        if provider == "gemini":
            api_key = APIConfig.get_api_key("gemini")
            return GeminiModelRegistry.get_model_info(model_id, api_key)
        return None


# Made with Bob