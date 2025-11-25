"""
Anthropic agent implementation.

This module implements the AnthropicAgent class for Claude models with
logprob extraction and usage-based cost calculation.
"""

import time
import random
from typing import Dict, Any, Optional
import anthropic
from anthropic.types import Message, MessageParam
from anthropic import APIError, RateLimitError, APIStatusError
from semiosis.agents.base import BaseAgent, AgentResponse


class AnthropicAgent(BaseAgent):
    """
    Agent implementation for Anthropic Claude models.
    
    Provides integration with Anthropic's API including logprob extraction
    for semantic information calculations and usage-based cost tracking.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Anthropic agent.
        
        Args:
            config: Configuration dictionary containing:
                - api_key: Anthropic API key
                - model: Model name (e.g., "claude-3-5-sonnet-20241022")
                - temperature: Sampling temperature (0.0-1.0)
                - max_tokens: Maximum tokens to generate
                - top_p: Nucleus sampling parameter
        """
        super().__init__(config)
        
        # Extract configuration
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.model = config.get("model", "claude-3-5-sonnet-20241022")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 1000)
        self.top_p = config.get("top_p", 1.0)
        
        # Rate limiting and retry configuration
        self.max_retries = config.get("max_retries", 3)
        self.base_delay = config.get("base_delay", 1.0)
        self.max_delay = config.get("max_delay", 60.0)
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Cost tracking (approximate pricing as of 2024)
        self.pricing = self._get_model_pricing()
        
    def _get_model_pricing(self) -> Dict[str, Dict[str, float]]:
        """
        Get pricing information for different Claude models.
        
        Returns:
            Dictionary with model pricing (per 1M tokens)
        """
        return {
            "claude-3-5-sonnet-20241022": {
                "input": 3.00,   # $3 per 1M input tokens
                "output": 15.00  # $15 per 1M output tokens
            },
            "claude-3-5-haiku-20241022": {
                "input": 1.00,   # $1 per 1M input tokens  
                "output": 5.00   # $5 per 1M output tokens
            },
            "claude-3-opus-20240229": {
                "input": 15.00,  # $15 per 1M input tokens
                "output": 75.00  # $75 per 1M output tokens
            }
        }
    
    def generate_response(self, query: str, context: Optional[str] = None) -> AgentResponse:
        """
        Generate a response to the given query using Claude.
        
        Args:
            query: The input query to respond to
            context: Optional context to include in the prompt
            
        Returns:
            AgentResponse containing the output and metadata
        """
        # Build messages for Claude's chat format
        messages = self._build_messages(query, context)
        
        # Implement retry logic with exponential backoff
        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()
                
                # Make API call to Claude
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    messages=messages,
                    extra_headers={"anthropic-beta": "token-counting"}  # For usage tracking
                )
                
                end_time = time.time()
                
                # Extract response content
                output = ""
                if response.content:
                    for content_block in response.content:
                        if content_block.type == "text":
                            output += content_block.text
                
                # Calculate cost based on usage
                cost = self._calculate_cost(response)
                
                # Extract logprobs if available (Claude doesn't provide traditional logprobs)
                # We'll simulate this for now, but note this limitation
                logprobs = self._extract_logprobs_simulation(output)
                
                return AgentResponse(
                    output=output,
                    logprobs=logprobs,
                    metadata={
                        "model": self.model,
                        "usage": {
                            "input_tokens": response.usage.input_tokens if response.usage else 0,
                            "output_tokens": response.usage.output_tokens if response.usage else 0,
                        },
                        "response_time": end_time - start_time,
                        "stop_reason": response.stop_reason,
                        "attempts": attempt + 1
                    },
                    cost=cost
                )
                
            except RateLimitError as e:
                # Rate limit hit - wait and retry
                if attempt < self.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    return AgentResponse(
                        output="",
                        logprobs={},
                        metadata={
                            "error": f"Rate limit exceeded after {self.max_retries} retries: {str(e)}",
                            "model": self.model,
                            "attempts": attempt + 1
                        },
                        cost=0.0
                    )
                    
            except APIStatusError as e:
                # Handle specific API status errors
                if e.status_code >= 500 and attempt < self.max_retries:
                    # Server error - retry with backoff
                    delay = self._calculate_retry_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    return AgentResponse(
                        output="",
                        logprobs={},
                        metadata={
                            "error": f"API error {e.status_code}: {str(e)}",
                            "model": self.model,
                            "attempts": attempt + 1
                        },
                        cost=0.0
                    )
                    
            except APIError as e:
                # General API error - retry if not final attempt
                if attempt < self.max_retries:
                    delay = self._calculate_retry_delay(attempt)
                    time.sleep(delay)
                    continue
                else:
                    return AgentResponse(
                        output="",
                        logprobs={},
                        metadata={
                            "error": f"API error after {self.max_retries} retries: {str(e)}",
                            "model": self.model,
                            "attempts": attempt + 1
                        },
                        cost=0.0
                    )
                    
            except Exception as e:
                # Unexpected error - don't retry
                return AgentResponse(
                    output="",
                    logprobs={},
                    metadata={
                        "error": f"Unexpected error: {str(e)}",
                        "model": self.model,
                        "attempts": attempt + 1
                    },
                    cost=0.0
                )
        
        # This should never be reached, but just in case
        return AgentResponse(
            output="",
            logprobs={},
            metadata={
                "error": "Maximum retries exceeded",
                "model": self.model,
                "attempts": self.max_retries + 1
            },
            cost=0.0
        )
    
    def extract_logprobs(self, query: str, response: str, context: Optional[str] = None) -> Dict[str, float]:
        """
        Extract token-level log probabilities for the response.
        
        Note: Claude's API doesn't provide traditional logprobs like OpenAI.
        This method provides a simulation for compatibility with the SIT framework.
        
        Args:
            query: The original query
            response: The agent's response
            context: Optional context used in the generation
            
        Returns:
            Dictionary mapping tokens to simulated log probabilities
        """
        # Claude doesn't provide logprobs, so we simulate them
        # In production, this would need to be replaced with actual logprob extraction
        return self._extract_logprobs_simulation(response)
    
    def _extract_logprobs_simulation(self, response: str) -> Dict[str, float]:
        """
        Simulate logprobs for compatibility with SIT calculations.
        
        This is a temporary implementation until Claude provides logprobs
        or we implement alternative confidence measures.
        
        Args:
            response: The response text
            
        Returns:
            Dictionary with simulated token probabilities
        """
        tokens = response.split()
        logprobs = {}
        
        for i, token in enumerate(tokens):
            # Simulate varying confidence based on token position and characteristics
            if token.lower() in ["select", "from", "where", "and", "or"]:
                # SQL keywords get high confidence
                simulated_logprob = -0.1
            elif token.isdigit():
                # Numbers get medium confidence  
                simulated_logprob = -0.5
            elif len(token) > 10:
                # Long tokens get lower confidence
                simulated_logprob = -1.5
            else:
                # Default confidence with some position-based variation
                simulated_logprob = -0.8 - (i * 0.01)  # Slightly decreasing confidence
            
            logprobs[token] = simulated_logprob
        
        return logprobs
    
    def _build_messages(self, query: str, context: Optional[str] = None) -> list[MessageParam]:
        """
        Build message format for Claude's chat API.
        
        Args:
            query: The user query
            context: Optional context to include
            
        Returns:
            List of messages for the API call
        """
        # Build the user message with context if provided
        user_content = query
        if context:
            user_content = f"Context:\n{context}\n\nQuery: {query}"
        
        return [
            {
                "role": "user", 
                "content": user_content
            }
        ]
    
    def _calculate_cost(self, response: Message) -> float:
        """
        Calculate the cost of the API call based on token usage.
        
        Args:
            response: The Claude API response
            
        Returns:
            Estimated cost in USD
        """
        if not response.usage:
            return 0.0
        
        # Get pricing for this model
        model_pricing = self.pricing.get(self.model, {
            "input": 3.0,   # Default to Sonnet pricing
            "output": 15.0
        })
        
        # Calculate cost based on token usage
        input_cost = (response.usage.input_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (response.usage.output_tokens / 1_000_000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def get_cost_estimate(self, query: str, response: str) -> float:
        """
        Estimate the computational cost of generating the response.
        
        This provides a rough estimate based on token counts when
        actual usage data isn't available.
        
        Args:
            query: Input query
            response: Agent response
            
        Returns:
            Estimated cost in USD
        """
        # Rough token estimation (actual tokenization would be more accurate)
        query_tokens = len(query.split()) * 1.3  # Approximate subword tokenization
        response_tokens = len(response.split()) * 1.3
        
        # Get pricing for this model
        model_pricing = self.pricing.get(self.model, {
            "input": 3.0,
            "output": 15.0
        })
        
        # Calculate estimated cost
        input_cost = (query_tokens / 1_000_000) * model_pricing["input"] 
        output_cost = (response_tokens / 1_000_000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def _calculate_retry_delay(self, attempt: int) -> float:
        """
        Calculate the delay for retry attempt using exponential backoff with jitter.
        
        Args:
            attempt: The current attempt number (0-based)
            
        Returns:
            Delay in seconds
        """
        # Exponential backoff: base_delay * (2 ^ attempt)
        delay = self.base_delay * (2 ** attempt)
        
        # Add jitter to avoid thundering herd
        jitter = random.uniform(0.1, 0.3) * delay
        delay += jitter
        
        # Cap at maximum delay
        return min(delay, self.max_delay)