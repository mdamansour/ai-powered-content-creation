"""
API key management for AI providers.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class APIConfig:
    """Manage API keys for different AI providers."""
    
    # AI Provider API Keys
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    @classmethod
    def get_active_provider(cls) -> Optional[str]:
        """
        Determine which AI provider is configured.
        
        Returns:
            str: Provider name ('gemini', 'openai', 'anthropic') or None
        """
        if cls.GEMINI_API_KEY:
            return "gemini"
        elif cls.OPENAI_API_KEY:
            return "openai"
        elif cls.ANTHROPIC_API_KEY:
            return "anthropic"
        return None
    
    @classmethod
    def is_configured(cls, provider: str = None) -> bool:
        """
        Check if a specific provider or any provider is configured.
        
        Args:
            provider: Provider name to check, or None to check any
            
        Returns:
            bool: True if configured, False otherwise
        """
        if provider is None:
            return cls.get_active_provider() is not None
        
        provider = provider.lower()
        if provider == "gemini":
            return cls.GEMINI_API_KEY is not None
        elif provider == "openai":
            return cls.OPENAI_API_KEY is not None
        elif provider == "anthropic":
            return cls.ANTHROPIC_API_KEY is not None
        return False
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """
        Get API key for a specific provider.
        
        Args:
            provider: Provider name ('gemini', 'openai', 'anthropic')
            
        Returns:
            str: API key or None if not configured
        """
        provider = provider.lower()
        if provider == "gemini":
            return cls.GEMINI_API_KEY
        elif provider == "openai":
            return cls.OPENAI_API_KEY
        elif provider == "anthropic":
            return cls.ANTHROPIC_API_KEY
        return None
    
    @classmethod
    def set_api_key(cls, provider: str, api_key: str):
        """
        Set API key for a provider (runtime only, doesn't persist).
        
        Args:
            provider: Provider name
            api_key: API key value
        """
        provider = provider.lower()
        if provider == "gemini":
            cls.GEMINI_API_KEY = api_key
            os.environ["GEMINI_API_KEY"] = api_key
        elif provider == "openai":
            cls.OPENAI_API_KEY = api_key
            os.environ["OPENAI_API_KEY"] = api_key
        elif provider == "anthropic":
            cls.ANTHROPIC_API_KEY = api_key
            os.environ["ANTHROPIC_API_KEY"] = api_key
    
    @classmethod
    def validate_key_format(cls, provider: str, api_key: str) -> bool:
        """
        Basic validation of API key format.
        
        Args:
            provider: Provider name
            api_key: API key to validate
            
        Returns:
            bool: True if format looks valid
        """
        if not api_key or len(api_key) < 10:
            return False
        
        provider = provider.lower()
        if provider == "gemini":
            # Gemini keys typically start with specific prefixes
            return len(api_key) > 20
        elif provider == "openai":
            # OpenAI keys start with 'sk-'
            return api_key.startswith("sk-")
        elif provider == "anthropic":
            # Anthropic keys start with 'sk-ant-'
            return api_key.startswith("sk-ant-")
        
        return True  # Unknown provider, assume valid

# Made with Bob
