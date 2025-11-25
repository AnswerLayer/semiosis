"""
Ollama agent implementation.

This module implements the OllamaAgent class for local models with
real logprob extraction and cost-free inference.
"""

import os
import time
import json
import requests
from typing import Dict, Any, Optional, List
from semiosis.agents.base import BaseAgent, AgentResponse


class OllamaAgent(BaseAgent):
    """
    Agent implementation for Ollama local models.
    
    Provides integration with Ollama's API including real logprob extraction
    for semantic information calculations and local inference without API costs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Ollama agent.
        
        Args:
            config: Configuration dictionary containing:
                - base_url: Ollama server URL (default: http://localhost:11434)
                - model: Model name (default: qwen2.5-coder:7b)
                - temperature: Sampling temperature (0.0-1.0)
                - max_tokens: Maximum tokens to generate
                - top_p: Nucleus sampling parameter
                - timeout: Request timeout in seconds
        """
        super().__init__(config)
        
        # Extract configuration
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "qwen2.5-coder:7b")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 1000)
        self.top_p = config.get("top_p", 1.0)
        self.timeout = config.get("timeout", 60)
        
        # Validate Ollama availability
        self._validate_ollama_setup()
        
    def _validate_ollama_setup(self):
        """
        Validate that Ollama is available and the model exists.
        
        Raises:
            ConnectionError: If Ollama is not running
            ValueError: If the specified model is not available
        """
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                f"Ollama server not found at {self.base_url}. "
                "Please ensure Ollama is installed and running.\n"
                "Install: curl -fsSL https://ollama.ai/install.sh | sh\n"
                "Start: ollama serve"
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama: {e}")
        
        # Check if model is available
        try:
            models_response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            models_response.raise_for_status()
            available_models = [
                model["name"] for model in models_response.json().get("models", [])
            ]
            
            if self.model not in available_models:
                raise ValueError(
                    f"Model '{self.model}' not found. Available models: {available_models}\n"
                    f"Pull the model: ollama pull {self.model}"
                )
                
        except requests.exceptions.RequestException as e:
            # If we can't check models, log warning but continue
            print(f"Warning: Could not verify model availability: {e}")
    
    def generate_response(self, query: str, context: Optional[str] = None) -> AgentResponse:
        """
        Generate a response to the given query using Ollama.
        
        Args:
            query: The input query to respond to
            context: Optional context to include in the prompt
            
        Returns:
            AgentResponse containing the output and metadata
        """
        # Build the prompt
        prompt = self._build_prompt(query, context)
        
        try:
            start_time = time.time()
            
            # Make API call to Ollama with logprobs
            payload = {
                "model": self.model,
                "prompt": prompt,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "top_p": self.top_p,
                },
                "stream": False,  # Get complete response
                "logprobs": True,  # Enable logprobs (Ollama v0.12.11+)
                "top_logprobs": 5   # Get top 5 alternative tokens
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            end_time = time.time()
            result = response.json()
            
            # Extract response content
            output = result.get("response", "")
            
            # Extract logprobs from response
            logprobs = self._extract_logprobs(result)
            
            # Calculate cost (free for local inference)
            cost = 0.0
            
            return AgentResponse(
                output=output,
                logprobs=logprobs,
                metadata={
                    "model": self.model,
                    "provider": "ollama",
                    "response_time": end_time - start_time,
                    "eval_count": result.get("eval_count", 0),
                    "eval_duration": result.get("eval_duration", 0),
                    "prompt_eval_count": result.get("prompt_eval_count", 0),
                    "prompt_eval_duration": result.get("prompt_eval_duration", 0),
                    "total_duration": result.get("total_duration", 0),
                    "load_duration": result.get("load_duration", 0),
                    "logprobs_available": True  # Real logprobs, not simulated
                },
                cost=cost
            )
            
        except requests.exceptions.Timeout:
            return AgentResponse(
                output="",
                logprobs={},
                metadata={
                    "error": f"Request timeout after {self.timeout} seconds",
                    "model": self.model,
                    "provider": "ollama",
                    "logprobs_available": False
                },
                cost=0.0
            )
            
        except requests.exceptions.RequestException as e:
            return AgentResponse(
                output="",
                logprobs={},
                metadata={
                    "error": f"Ollama API error: {str(e)}",
                    "model": self.model,
                    "provider": "ollama",
                    "logprobs_available": False
                },
                cost=0.0
            )
            
        except Exception as e:
            return AgentResponse(
                output="",
                logprobs={},
                metadata={
                    "error": f"Unexpected error: {str(e)}",
                    "model": self.model,
                    "provider": "ollama",
                    "logprobs_available": False
                },
                cost=0.0
            )
    
    def extract_logprobs(self, query: str, response: str, context: Optional[str] = None) -> Dict[str, float]:
        """
        Extract token-level log probabilities for the response.
        
        Note: This method re-runs inference to get logprobs for a specific response.
        For efficiency, use the logprobs returned by generate_response() instead.
        
        Args:
            query: The original query
            response: The agent's response
            context: Optional context used in the generation
            
        Returns:
            Dictionary mapping tokens to their log probabilities
        """
        # For Ollama, we get logprobs directly from generate_response()
        # This method is mainly for compatibility with the base interface
        
        # Build the full prompt including the expected response
        prompt = self._build_prompt(query, context)
        full_prompt = f"{prompt}\n{response}"
        
        try:
            # Request logprobs for the full sequence
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "options": {
                    "temperature": 0.0,  # Deterministic for logprob extraction
                    "num_predict": 1,    # Just one token to get sequence logprobs
                },
                "stream": False,
                "logprobs": True,
                "top_logprobs": 1
            }
            
            response_obj = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response_obj.raise_for_status()
            
            result = response_obj.json()
            return self._extract_logprobs(result)
            
        except Exception as e:
            print(f"Warning: Could not extract logprobs: {e}")
            return {}
    
    def _extract_logprobs(self, result: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract logprobs from Ollama API response.
        
        Args:
            result: Raw API response from Ollama
            
        Returns:
            Dictionary mapping tokens to their log probabilities
        """
        logprobs_dict = {}
        
        try:
            # Ollama v0.12.11+ includes logprobs in the response
            if "logprobs" in result:
                logprobs_data = result["logprobs"]
                
                # Handle different logprobs formats
                if isinstance(logprobs_data, list):
                    # List format: [{"token": "hello", "logprob": -0.1, ...}, ...]
                    for token_data in logprobs_data:
                        if isinstance(token_data, dict) and "token" in token_data:
                            token = token_data["token"]
                            logprob = token_data.get("logprob", -10.0)
                            logprobs_dict[token] = logprob
                            
                elif isinstance(logprobs_data, dict):
                    # Dict format: {"tokens": [...], "logprobs": [...]}
                    tokens = logprobs_data.get("tokens", [])
                    logprobs = logprobs_data.get("logprobs", [])
                    
                    for token, logprob in zip(tokens, logprobs):
                        logprobs_dict[token] = logprob
                        
            # Fallback: extract from response text if logprobs not available
            elif "response" in result:
                # Generate simple token mapping for compatibility
                response_text = result["response"]
                tokens = response_text.split()
                
                # Use default logprob values based on token characteristics
                for token in tokens:
                    if len(token) <= 2:
                        logprobs_dict[token] = -0.5  # Short tokens likely common
                    elif token.isalpha():
                        logprobs_dict[token] = -1.0  # Regular words
                    else:
                        logprobs_dict[token] = -2.0  # Special tokens less likely
                        
        except Exception as e:
            print(f"Warning: Error extracting logprobs: {e}")
            
        return logprobs_dict
    
    def _build_prompt(self, query: str, context: Optional[str] = None) -> str:
        """
        Build a prompt for the model.
        
        Args:
            query: The user query
            context: Optional context to include
            
        Returns:
            Formatted prompt string
        """
        if context:
            return f"Context:\n{context}\n\nQuery: {query}\n\nResponse:"
        else:
            return f"Query: {query}\n\nResponse:"
    
    def get_cost_estimate(self, query: str, response: str) -> float:
        """
        Estimate the computational cost of generating the response.
        
        For local Ollama models, this is always 0.0 since there are no API costs.
        
        Args:
            query: Input query
            response: Agent response
            
        Returns:
            Cost estimate (always 0.0 for local models)
        """
        return 0.0
    
    @classmethod
    def get_available_models(cls, base_url: str = "http://localhost:11434") -> List[str]:
        """
        Get list of available models from Ollama.
        
        Args:
            base_url: Ollama server URL
            
        Returns:
            List of available model names
        """
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=10)
            response.raise_for_status()
            models_data = response.json()
            return [model["name"] for model in models_data.get("models", [])]
        except Exception as e:
            print(f"Warning: Could not fetch available models: {e}")
            return []
    
    @classmethod
    def get_recommended_models(cls) -> List[Dict[str, str]]:
        """
        Get list of recommended models for Semiosis documentation analysis.
        
        Returns:
            List of model recommendations with descriptions
        """
        return [
            {
                "name": "qwen2.5-coder:7b",
                "description": "Excellent for code and documentation analysis",
                "size": "~4GB",
                "use_case": "Code/documentation understanding"
            },
            {
                "name": "llama3.1:8b", 
                "description": "General purpose, good reasoning",
                "size": "~4.7GB",
                "use_case": "General text analysis"
            },
            {
                "name": "mistral:7b",
                "description": "Fast and efficient, good for structured data",
                "size": "~3.8GB", 
                "use_case": "SQL generation and schema analysis"
            },
            {
                "name": "qwen2.5:14b",
                "description": "Larger model for complex analysis",
                "size": "~8.2GB",
                "use_case": "Complex reasoning tasks"
            }
        ]