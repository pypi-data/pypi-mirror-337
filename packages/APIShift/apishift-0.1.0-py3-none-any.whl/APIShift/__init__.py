# Multi-LLM Manager Package
from .conversation import Conversation
from .providers import (
    LLMProvider, 
    GeminiProvider, 
    OpenRouterProvider, 
    GroqProvider
)
from .exceptions import (
    MultiLLMManagerError,
    RateLimitError,
    QuotaExceededError,
    NoAvailableProvidersError,
    ProviderInitializationError
)

__version__ = "0.1.0"

__all__ = [
    # Main classes
    'Conversation',
    'LLMProvider',
    'GeminiProvider',
    'OpenRouterProvider',
    'GroqProvider',
    
    # Exceptions
    'MultiLLMManagerError',
    'RateLimitError',
    'QuotaExceededError',
    'NoAvailableProvidersError',
    'ProviderInitializationError'
]
