class MultiLLMManagerError(Exception):
    """Base exception for multi_llm_manager package."""
    pass

class RateLimitError(MultiLLMManagerError):
    """Raised when an API rate limit is exceeded."""
    def __init__(self, provider, message="Rate limit exceeded"):
        self.provider = provider
        self.message = f"{provider} {message}"
        super().__init__(self.message)

class QuotaExceededError(MultiLLMManagerError):
    """Raised when a provider's daily/monthly quota is exhausted."""
    def __init__(self, provider, message="Quota exceeded"):
        self.provider = provider
        self.message = f"{provider} {message}"
        super().__init__(self.message)

class NoAvailableProvidersError(MultiLLMManagerError):
    """Raised when no providers are available to handle the request."""
    def __init__(self, message="No available providers"):
        super().__init__(message)

class ProviderInitializationError(MultiLLMManagerError):
    """Raised when a provider fails to initialize."""
    def __init__(self, provider, message="Provider initialization failed"):
        self.provider = provider
        self.message = f"{provider} {message}"
        super().__init__(self.message)
