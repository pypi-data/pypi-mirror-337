"""
LLM connector module for integrating with multiple providers.

This module provides a unified interface for communicating with various
LLM providers such as OpenAI and Anthropic, with secure API authentication
and the ability to compare outputs from multiple models.
"""

import os
import json
import uuid
import hashlib
import base64
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
from pathlib import Path
import logging

# Optional dependencies
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .core import RuleSet

class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"  # For testing

class ApiCredentialManager:
    """Securely manages API credentials for LLM providers."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ApiCredentialManager, cls).__new__(cls)
            cls._instance._credentials = {}
            cls._instance._secure_storage_path = Path.home() / ".cursor-rules" / "credentials"
            cls._instance._secure_storage_path.parent.mkdir(exist_ok=True, parents=True)
            cls._instance._load_credentials()
        return cls._instance
    
    def _load_credentials(self) -> None:
        """Load stored credentials if available."""
        if self._secure_storage_path.exists():
            try:
                with open(self._secure_storage_path, 'r') as f:
                    encoded_data = f.read().strip()
                    if encoded_data:
                        # Simple obfuscation, not secure encryption
                        decoded = base64.b64decode(encoded_data).decode('utf-8')
                        self._credentials = json.loads(decoded)
            except Exception:
                # If any error occurs, start with empty credentials
                self._credentials = {}
    
    def _save_credentials(self) -> None:
        """Save credentials to storage."""
        try:
            # Simple obfuscation, not secure encryption
            encoded = base64.b64encode(json.dumps(self._credentials).encode('utf-8')).decode('utf-8')
            with open(self._secure_storage_path, 'w') as f:
                f.write(encoded)
        except Exception as e:
            print(f"Warning: Failed to save credentials: {e}")
    
    def set_api_key(self, provider: LLMProvider, api_key: str) -> None:
        """Set API key for a provider."""
        self._credentials[provider] = {"api_key": api_key}
        self._save_credentials()
    
    def get_api_key(self, provider: LLMProvider) -> Optional[str]:
        """Get API key for a provider."""
        if provider in self._credentials:
            return self._credentials[provider].get("api_key")
        
        # Fallback to environment variables
        if provider == LLMProvider.OPENAI:
            return os.environ.get("OPENAI_API_KEY")
        elif provider == LLMProvider.ANTHROPIC:
            return os.environ.get("ANTHROPIC_API_KEY")
        
        return None
    
    def clear_api_key(self, provider: LLMProvider) -> None:
        """Clear API key for a provider."""
        if provider in self._credentials:
            del self._credentials[provider]
            self._save_credentials()

@dataclass
class LLMRequest:
    """A request to an LLM provider."""
    prompt: str
    system_message: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    provider: LLMProvider = LLMProvider.OPENAI
    model: Optional[str] = None  # If None, use provider's default
    stop_sequences: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_default_model(self) -> str:
        """Get the default model for the selected provider."""
        if self.provider == LLMProvider.OPENAI:
            return "gpt-4-turbo"
        elif self.provider == LLMProvider.ANTHROPIC:
            return "claude-3-7-sonnet-latest"
        elif self.provider == LLMProvider.MOCK:
            return "mock-model"
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

@dataclass
class LLMResponse:
    """A response from an LLM provider."""
    text: str
    provider: LLMProvider
    model: str
    request_id: str
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    elapsed_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_response: Any = None  # The raw response from the provider

class LLMConnector:
    """Connects to various LLM providers with a unified interface."""
    
    def __init__(self):
        self.credential_manager = ApiCredentialManager()
        self._verify_dependencies()
    
    def _verify_dependencies(self) -> None:
        """Verify that necessary dependencies are installed."""
        missing = []
        if not OPENAI_AVAILABLE:
            missing.append("openai")
        if not ANTHROPIC_AVAILABLE:
            missing.append("anthropic")
        
        if missing:
            print(f"Warning: The following packages are not installed: {', '.join(missing)}")
            print("Some LLM providers may not be available.")
    
    def set_api_key(self, provider: LLMProvider, api_key: str) -> None:
        """Set API key for a provider."""
        self.credential_manager.set_api_key(provider, api_key)
    
    def get_api_key(self, provider: LLMProvider) -> Optional[str]:
        """Get API key for a provider."""
        return self.credential_manager.get_api_key(provider)
    
    def get_default_model(self, provider: LLMProvider) -> str:
        """Get the default model for the selected provider."""
        if provider == LLMProvider.OPENAI:
            return "gpt-4-turbo"
        elif provider == LLMProvider.ANTHROPIC:
            return "claude-3-7-sonnet-latest"
        elif provider == LLMProvider.MOCK:
            return "mock-model"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def is_provider_available(self, provider: LLMProvider) -> bool:
        """Check if a provider is available (package installed and API key set)."""
        if provider == LLMProvider.OPENAI:
            return OPENAI_AVAILABLE and self.get_api_key(provider) is not None
        elif provider == LLMProvider.ANTHROPIC:
            return ANTHROPIC_AVAILABLE and self.get_api_key(provider) is not None
        elif provider == LLMProvider.MOCK:
            return True
        return False
    
    def list_available_providers(self) -> List[LLMProvider]:
        """List all available providers."""
        return [p for p in LLMProvider if self.is_provider_available(p)]
    
    def request(self, request: LLMRequest) -> LLMResponse:
        """Send a request to the LLM provider and return the response."""
        if not self.is_provider_available(request.provider):
            available = self.list_available_providers()
            available_str = ", ".join([p.value for p in available]) if available else "none"
            raise ValueError(f"Provider {request.provider.value} is not available. Available providers: {available_str}")
        
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        
        # Get the appropriate model for the provider
        model = request.model
        if not model:
            model = self.get_default_model(request.provider)
        
        print(f"\n--- LLM Request Details ---")
        print(f"Provider: {request.provider.value}")
        print(f"Model: {model}")
        print(f"System message length: {len(request.system_message) if request.system_message else 0} chars")
        print(f"Prompt length: {len(request.prompt)} chars")
        # Check if prompt appears to be truncated
        if len(request.prompt) < 50:
            print(f"WARNING: Prompt appears to be very short: '{request.prompt}'")
        
        # Dispatch to the appropriate handler for the provider
        try:
            if request.provider == LLMProvider.OPENAI:
                response = self._request_openai(request, model, request_id)
            elif request.provider == LLMProvider.ANTHROPIC:
                response = self._request_anthropic(request)
            elif request.provider == LLMProvider.MOCK:
                response = self._request_mock(request, model, request_id)
            else:
                raise ValueError(f"Unsupported provider: {request.provider}")
            
            print(f"Response tokens: {response.total_tokens}")
            print(f"Response length: {len(response.text)} chars")
            return response
        except Exception as e:
            print(f"Error in LLM request: {type(e).__name__}: {e}")
            raise
    
    def _request_openai(self, request: LLMRequest, model: str, request_id: str) -> LLMResponse:
        """Send a request to OpenAI."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package is not installed")
        
        api_key = self.get_api_key(LLMProvider.OPENAI)
        if not api_key:
            raise ValueError("OpenAI API key is not set")
        
        client = openai.OpenAI(api_key=api_key)
        
        messages = []
        if request.system_message:
            messages.append({"role": "system", "content": request.system_message})
        
        messages.append({"role": "user", "content": request.prompt})
        
        # Measure request time
        start_time = time.time()
        
        raw_response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stop=request.stop_sequences if request.stop_sequences else None
        )
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        return LLMResponse(
            text=raw_response.choices[0].message.content,
            provider=LLMProvider.OPENAI,
            model=model,
            request_id=request_id,
            completion_tokens=raw_response.usage.completion_tokens,
            prompt_tokens=raw_response.usage.prompt_tokens,
            total_tokens=raw_response.usage.total_tokens,
            elapsed_time=elapsed_time,
            metadata=request.metadata,
            raw_response=raw_response
        )
    
    def _request_anthropic(self, request: LLMRequest) -> LLMResponse:
        """
        Handle a request to the Anthropic API.
        
        Args:
            request: LLMRequest object containing all request parameters
            
        Returns:
            LLMResponse object with the response from the API
        """
        from yaspin import yaspin
        from yaspin.spinners import Spinners
        
        api_key = self.get_api_key(LLMProvider.ANTHROPIC)
        
        # Use the default model if none is specified
        model = request.model or self.get_default_model(LLMProvider.ANTHROPIC)
        
        # Create the client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Format the messages
        messages = [
            {"role": "system", "content": request.system_message},
            {"role": "user", "content": request.prompt}
        ]
        
        # Set parameters
        params = {
            "model": model,
            "messages": messages,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            # No stream parameter, it's not part of LLMRequest
        }
        
        # Make the request and measure elapsed time
        start_time = time.time()
        try:
            # Show a spinner while waiting for the API response
            with yaspin(Spinners.dots, text=f"Waiting for {model} response...") as spinner:
                response = client.messages.create(**params)
                spinner.ok("✓")
                
            elapsed_time = time.time() - start_time
        
            # Create the response object
            llm_response = LLMResponse(
                provider=LLMProvider.ANTHROPIC,
                model=model,
                text=response.content[0].text,
                completion_tokens=response.usage.output_tokens,
                prompt_tokens=response.usage.input_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                elapsed_time=elapsed_time,
                request_id=str(uuid.uuid4()),  # Generate a request ID
                metadata=request.metadata,
                raw_response=response
            )
            
            return llm_response
        except Exception as e:
            # Log the error and re-raise
            logging.error(f"Error using Anthropic API: {e}")
            raise
    
    def _request_mock(self, request: LLMRequest, model: str, request_id: str) -> LLMResponse:
        """Mock LLM response for testing."""
        # Measure request time
        start_time = time.time()
        
        # Simulate thinking time
        time.sleep(0.5)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        return LLMResponse(
            text=f"Mock response to: {request.prompt[:50]}...",
            provider=LLMProvider.MOCK,
            model=model,
            request_id=request_id,
            completion_tokens=100,
            prompt_tokens=len(request.prompt.split()),
            total_tokens=100 + len(request.prompt.split()),
            elapsed_time=elapsed_time,
            metadata=request.metadata,
            raw_response=None
        )

class MultiLLMProcessor:
    """Process requests with multiple LLMs and compare results."""
    
    def __init__(self):
        self.connector = LLMConnector()
    
    def process_with_all_available(self, request: LLMRequest) -> List[LLMResponse]:
        """Process a request with all available providers."""
        providers = self.connector.list_available_providers()
        responses = []
        
        for provider in providers:
            provider_request = LLMRequest(
                prompt=request.prompt,
                system_message=request.system_message,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                provider=provider,
                model=request.model,
                stop_sequences=request.stop_sequences,
                metadata=request.metadata
            )
            
            try:
                response = self.connector.request(provider_request)
                responses.append(response)
            except Exception as e:
                print(f"Error with provider {provider}: {e}")
        
        return responses
    
    def process_with_specific(self, request: LLMRequest, providers: List[LLMProvider]) -> List[LLMResponse]:
        """Process a request with specific providers."""
        responses = []
        
        for provider in providers:
            if not self.connector.is_provider_available(provider):
                print(f"Provider {provider} is not available, skipping")
                continue
                
            provider_request = LLMRequest(
                prompt=request.prompt,
                system_message=request.system_message,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                provider=provider,
                model=request.model,
                stop_sequences=request.stop_sequences,
                metadata=request.metadata
            )
            
            try:
                response = self.connector.request(provider_request)
                responses.append(response)
            except Exception as e:
                print(f"Error with provider {provider}: {e}")
        
        return responses
    
    def select_best_response(self, responses: List[LLMResponse], 
                             criteria: Callable[[LLMResponse], float]) -> Optional[LLMResponse]:
        """
        Select the best response based on a scoring function.
        
        Args:
            responses: List of LLM responses
            criteria: A function that takes an LLMResponse and returns a score (higher is better)
            
        Returns:
            The response with the highest score, or None if responses is empty
        """
        if not responses:
            return None
            
        return max(responses, key=criteria)
    
    def generate_rules_with_multiple_llms(self, prompt: str, providers: List[LLMProvider] = None) -> Tuple[RuleSet, Dict[str, Any]]:
        """
        Generate a ruleset using multiple LLMs and select the best one.
        
        Args:
            prompt: The prompt to send to the LLMs
            providers: Specific providers to use, or None for all available
            
        Returns:
            A tuple of (selected ruleset, metadata dictionary with all responses)
        """
        system_message = """
        You are an expert at creating rules for AI assistants. 
        Generate a comprehensive set of rules based on the project description provided.
        Format your response as a valid JSON object with the following structure:
        {
            "name": "Project Rules",
            "description": "Rules for the project",
            "rules": [
                {"content": "Rule 1 description", "tags": ["tag1", "tag2"]},
                {"content": "Rule 2 description", "tags": ["tag3"]}
            ]
        }
        """
        
        request = LLMRequest(
            prompt=prompt,
            system_message=system_message,
            temperature=0.2,  # Lower temperature for more deterministic responses
            max_tokens=4000,
            metadata={"purpose": "ruleset_generation"}
        )
        
        # Get responses from providers
        if providers:
            responses = self.process_with_specific(request, providers)
        else:
            responses = self.process_with_all_available(request)
        
        if not responses:
            raise ValueError("No valid responses received from any provider")
        
        # Parse responses to RuleSets
        rulesets = {}
        for response in responses:
            try:
                ruleset_json = json.loads(response.text)
                ruleset = RuleSet(
                    name=ruleset_json.get("name", "Generated Rules"),
                    description=ruleset_json.get("description", "")
                )
                
                for rule_data in ruleset_json.get("rules", []):
                    ruleset.add_rule(rule_data.get("content", ""), tags=rule_data.get("tags", []))
                
                rulesets[response.provider] = {
                    "ruleset": ruleset,
                    "response": response
                }
            except Exception as e:
                print(f"Failed to parse ruleset from {response.provider}: {e}")
        
        # Select best ruleset based on number of rules
        best_provider = max(rulesets.keys(), 
                            key=lambda p: len(rulesets[p]["ruleset"].rules),
                            default=None)
        
        if not best_provider:
            raise ValueError("Could not generate a valid ruleset from any provider")
        
        metadata = {
            "all_responses": {p: r["response"] for p, r in rulesets.items()},
            "selected_provider": best_provider
        }
        
        return rulesets[best_provider]["ruleset"], metadata 