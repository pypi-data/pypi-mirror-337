import abc
import requests
from typing import List, Dict, Any, Optional
from .exceptions import RateLimitError, QuotaExceededError, ProviderInitializationError

class LLMProvider(abc.ABC):
    """Abstract base class for Language Model Providers."""
    
    def __init__(self, api_keys: List[str]):
        """
        Initialize the provider with a list of API keys.
        
        :param api_keys: List of API keys for the provider
        """
        if not api_keys:
            raise ProviderInitializationError(
                self.__class__.__name__, 
                "No API keys provided"
            )
        self.api_keys = api_keys
        self.current_key_index = 0
    
    def rotate_key(self):
        """
        Rotate to the next API key.
        
        :raises ProviderInitializationError: If no more keys are available
        """
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
    
    @abc.abstractmethod
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.
        
        :param messages: Conversation history
        :param kwargs: Additional generation parameters
        :return: Generated response
        """
        pass
    
    @abc.abstractmethod
    def _detect_rate_limit(self, response: Any) -> bool:
        """
        Detect if the response indicates a rate limit error.
        
        :param response: API response
        :return: True if rate limited, False otherwise
        """
        pass
    
    @abc.abstractmethod
    def _detect_quota_exceeded(self, response: Any) -> bool:
        """
        Detect if the response indicates a quota exceeded error.
        
        :param response: API response
        :return: True if quota exceeded, False otherwise
        """
        pass

class GeminiProvider(LLMProvider):
    """Provider for Google Gemini API."""
    
    def __init__(self, api_keys: List[str]):
        """
        Initialize Gemini provider.
        
        :param api_keys: List of Google AI API keys
        """
        try:
            import google.generativeai as genai
        except ImportError:
            raise ProviderInitializationError(
                "GeminiProvider", 
                "google-generativeai package not installed"
            )
        
        super().__init__(api_keys)
        self.model_name = "gemini-1.5-flash"
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """
        Generate response using Gemini API.
        
        :param messages: Conversation history
        :param kwargs: Additional generation parameters
        :return: Generated response
        :raises RateLimitError: If rate limit is exceeded
        :raises QuotaExceededError: If quota is exceeded
        """
        import google.generativeai as genai
        
        # Set the current API key
        genai.configure(api_key=self.api_keys[self.current_key_index])
        
        # Convert messages to Gemini's format
        formatted_messages = [
            {'role': msg['role'], 'parts': [msg['content']]} 
            for msg in messages
        ]
        
        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(
                formatted_messages[-1]['parts'][0],  # Send last message
                **kwargs
            )
            
            # Check for safety issues or errors
            if not response.parts:
                raise Exception("No response generated")
            
            return response.text
        
        except Exception as e:
            # Detect and handle specific errors
            if self._detect_rate_limit(e):
                raise RateLimitError("GeminiProvider")
            elif self._detect_quota_exceeded(e):
                raise QuotaExceededError("GeminiProvider")
            raise
    
    def _detect_rate_limit(self, response: Any) -> bool:
        """
        Detect Gemini rate limit errors.
        
        :param response: Exception or response object
        :return: True if rate limited, False otherwise
        """
        error_str = str(response).lower()
        return any(phrase in error_str for phrase in [
            "rate limit", 
            "quota exceeded", 
            "too many requests"
        ])
    
    def _detect_quota_exceeded(self, response: Any) -> bool:
        """
        Detect Gemini quota exceeded errors.
        
        :param response: Exception or response object
        :return: True if quota exceeded, False otherwise
        """
        error_str = str(response).lower()
        return any(phrase in error_str for phrase in [
            "quota exhausted", 
            "daily limit reached"
        ])

class OpenRouterProvider(LLMProvider):
    """Provider for OpenRouter API."""
    
    def __init__(self, api_keys: List[str]):
        """
        Initialize OpenRouter provider.
        
        :param api_keys: List of OpenRouter API keys
        """
        super().__init__(api_keys)
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.1-8b-instruct:free"
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """
        Generate response using OpenRouter API.
        
        :param messages: Conversation history
        :param kwargs: Additional generation parameters
        :return: Generated response
        :raises RateLimitError: If rate limit is exceeded
        :raises QuotaExceededError: If quota is exceeded
        """
        headers = {
            "Authorization": f"Bearer {self.api_keys[self.current_key_index]}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload
            )
            
            # Check for errors
            if not response.ok:
                if self._detect_rate_limit(response):
                    raise RateLimitError("OpenRouterProvider")
                elif self._detect_quota_exceeded(response):
                    raise QuotaExceededError("OpenRouterProvider")
                response.raise_for_status()
            
            # Extract response text
            return response.json()['choices'][0]['message']['content']
        
        except requests.RequestException as e:
            # Detect and handle specific errors
            if self._detect_rate_limit(e):
                raise RateLimitError("OpenRouterProvider")
            elif self._detect_quota_exceeded(e):
                raise QuotaExceededError("OpenRouterProvider")
            raise
    
    def _detect_rate_limit(self, response: Any) -> bool:
        """
        Detect OpenRouter rate limit errors.
        
        :param response: Response or exception object
        :return: True if rate limited, False otherwise
        """
        error_str = str(response).lower()
        status_code = getattr(response, 'status_code', None)
        
        return (
            status_code == 429 or 
            any(phrase in error_str for phrase in [
                "rate limit", 
                "too many requests"
            ])
        )
    
    def _detect_quota_exceeded(self, response: Any) -> bool:
        """
        Detect OpenRouter quota exceeded errors.
        
        :param response: Response or exception object
        :return: True if quota exceeded, False otherwise
        """
        error_str = str(response).lower()
        return any(phrase in error_str for phrase in [
            "quota exceeded", 
            "daily limit", 
            "usage limit"
        ])

class GroqProvider(LLMProvider):
    """Provider for Groq API."""
    
    def __init__(self, api_keys: List[str]):
        """
        Initialize Groq provider.
        
        :param api_keys: List of Groq API keys
        """
        try:
            import groq
        except ImportError:
            raise ProviderInitializationError(
                "GroqProvider", 
                "groq package not installed"
            )
        
        super().__init__(api_keys)
        self.model = "llama3-8b-8192"  # Example model
    
    def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """
        Generate response using Groq API.
        
        :param messages: Conversation history
        :param kwargs: Additional generation parameters
        :return: Generated response
        :raises RateLimitError: If rate limit is exceeded
        :raises QuotaExceededError: If quota is exceeded
        """
        from groq import Groq
        
        client = Groq(api_key=self.api_keys[self.current_key_index])
        
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            # Extract response text
            return response.choices[0].message.content
        
        except Exception as e:
            # Detect and handle specific errors
            if self._detect_rate_limit(e):
                raise RateLimitError("GroqProvider")
            elif self._detect_quota_exceeded(e):
                raise QuotaExceededError("GroqProvider")
            raise
    
    def _detect_rate_limit(self, response: Any) -> bool:
        """
        Detect Groq rate limit errors.
        
        :param response: Exception or response object
        :return: True if rate limited, False otherwise
        """
        error_str = str(response).lower()
        return any(phrase in error_str for phrase in [
            "rate limit", 
            "too many requests"
        ])
    
    def _detect_quota_exceeded(self, response: Any) -> bool:
        """
        Detect Groq quota exceeded errors.
        
        :param response: Exception or response object
        :return: True if quota exceeded, False otherwise
        """
        error_str = str(response).lower()
        return any(phrase in error_str for phrase in [
            "quota exceeded", 
            "daily limit reached"
        ])