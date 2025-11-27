"""
Together AI agent implementation.

This module implements the TogetherAgent class for hosted open-source models
with real logprob extraction and competitive pricing for production use.
"""

import os
import time
from typing import Any, Dict, List, Optional, Tuple

import openai

from semiosis.agents.base import AgentResponse, BaseAgent


class TogetherAgent(BaseAgent):
    """
    Agent implementation for Together AI's hosted open-source models.

    Provides integration with Together AI's OpenAI-compatible API including
    real logprob extraction for semantic information calculations and
    cost-effective inference with open source models.
    """

    # Model pricing in USD per 1M tokens (input/output where different)
    # Only serverless models that don't require dedicated endpoints
    MODEL_PRICING = {
        # Llama Models (Serverless only)
        "meta-llama/Llama-3.1-8B-Instruct-Turbo": (0.18, 0.18),
        "meta-llama/Llama-3.1-70B-Instruct-Turbo": (0.88, 0.88),
        "meta-llama/Llama-3-8B-Instruct-Turbo": (0.10, 0.10),
        # Mistral Models (Serverless)
        "mistralai/Mistral-7B-Instruct-v0.3": (0.20, 0.20),
        "mistralai/Mixtral-8x7B-Instruct-v0.1": (0.60, 0.60),
        # Qwen Models (Often serverless)
        "Qwen/Qwen2.5-Coder-32B-Instruct": (0.30, 0.30),
        "Qwen/Qwen2.5-7B-Instruct": (0.15, 0.15),
        # Other Serverless Models
        "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO": (0.60, 0.60),
        "teknium/OpenHermes-2.5-Mistral-7B": (0.20, 0.20),
        "togethercomputer/RedPajama-INCITE-Chat-3B-v1": (0.10, 0.10),
        # Llama 3.2 models (likely serverless)
        "meta-llama/Llama-3.2-3B-Instruct-Turbo": (0.06, 0.06),
        "meta-llama/Llama-3.2-1B-Instruct-Turbo": (0.04, 0.04),
    }

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Together AI agent.

        Args:
            config: Configuration dictionary containing:
                - api_key: Together AI API key (optional, can use env var)
                - model: Model name (default: meta-llama/Llama-3.1-8B-Instruct-Turbo)
                - temperature: Sampling temperature (0.0-2.0)
                - max_tokens: Maximum tokens to generate
                - top_p: Nucleus sampling parameter
                - top_k: Top-k sampling parameter
                - logprobs: Number of top logprobs to return (0-20)
        """
        super().__init__(config)

        # Extract configuration
        self.api_key = config.get("api_key") or os.getenv("TOGETHER_API_KEY")
        self.model = config.get("model", "meta-llama/Llama-3.2-3B-Instruct-Turbo")
        self.temperature = config.get("temperature", 0.1)
        self.max_tokens = config.get("max_tokens", 1000)
        self.top_p = config.get("top_p", 1.0)
        self.top_k = config.get("top_k", 50)
        self.logprobs = config.get("logprobs", 5)  # Request top 5 logprobs

        # Validate API key
        if not self.api_key:
            raise ValueError(
                "Together AI API key required. Set TOGETHER_API_KEY environment "
                "variable or pass 'api_key' in config."
            )

        # Initialize OpenAI client for Together AI
        self.client = openai.OpenAI(
            api_key=self.api_key, base_url="https://api.together.xyz/v1"
        )

        # Validate model availability
        self._validate_model()

    def _validate_model(self):
        """
        Validate that the specified model is available and supported.

        Raises:
            ValueError: If the model is not recognized
        """
        if self.model not in self.MODEL_PRICING:
            available_models = list(self.MODEL_PRICING.keys())
            raise ValueError(
                f"Model '{self.model}' not recognized. Available models:\n"
                + "\n".join(f"  - {model}" for model in available_models[:10])
                + f"\n  ... and {len(available_models) - 10} more"
                if len(available_models) > 10
                else ""
            )

    def generate_response(
        self, query: str, context: Optional[str] = None
    ) -> AgentResponse:
        """
        Generate a response to the given query using Together AI.

        Args:
            query: The input query to respond to
            context: Optional context to include in the prompt

        Returns:
            AgentResponse containing the output and metadata
        """
        # Build messages
        messages = self._build_messages(query, context)

        try:
            start_time = time.time()

            # Make API call to Together AI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                logprobs=True,  # Enable logprobs
                top_logprobs=self.logprobs,  # Number of top logprobs to return
                stream=False,
            )

            end_time = time.time()

            # Extract response content
            output = response.choices[0].message.content or ""

            # Extract logprobs
            logprobs = self._extract_logprobs(response)

            # Calculate cost
            cost = self._calculate_cost(response)

            # Debug: Check if we got actual data
            has_logprobs = len(logprobs) > 0

            return AgentResponse(
                output=output,
                logprobs=logprobs,
                metadata={
                    "model": self.model,
                    "provider": "together",
                    "response_time": end_time - start_time,
                    "prompt_tokens": (
                        response.usage.prompt_tokens if response.usage else 0
                    ),
                    "completion_tokens": (
                        response.usage.completion_tokens if response.usage else 0
                    ),
                    "total_tokens": (
                        response.usage.total_tokens if response.usage else 0
                    ),
                    "finish_reason": response.choices[0].finish_reason,
                    "logprobs_available": has_logprobs,  # Real logprobs from API
                    "request_id": getattr(response, "id", None),
                },
                cost=cost,
            )

        except openai.APIError as e:
            return AgentResponse(
                output="",
                logprobs={},
                metadata={
                    "error": f"Together AI API error: {str(e)}",
                    "model": self.model,
                    "provider": "together",
                    "logprobs_available": False,
                },
                cost=0.0,
            )

        except Exception as e:
            return AgentResponse(
                output="",
                logprobs={},
                metadata={
                    "error": f"Unexpected error: {str(e)}",
                    "model": self.model,
                    "provider": "together",
                    "logprobs_available": False,
                },
                cost=0.0,
            )

    def extract_logprobs(
        self, query: str, response: str, context: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Extract token-level log probabilities for a specific response.

        Note: This method re-runs inference to get logprobs for a specific response.
        For efficiency, use the logprobs returned by generate_response() instead.

        Args:
            query: The original query
            response: The agent's response to get logprobs for
            context: Optional context used in the generation

        Returns:
            Dictionary mapping tokens to their log probabilities
        """
        # For hosted APIs, we typically can't get logprobs for arbitrary text
        # This method would need to use a different approach or return empty
        print("Warning: extract_logprobs not supported for hosted Together AI models")
        return {}

    def _extract_logprobs(self, response) -> Dict[str, float]:
        """
        Extract logprobs from Together AI API response.

        Args:
            response: Raw API response from Together AI

        Returns:
            Dictionary mapping tokens to their log probabilities
        """
        logprobs_dict = {}

        try:
            choice = response.choices[0]

            if hasattr(choice, "logprobs") and choice.logprobs:
                # Try OpenAI format (content) first
                if hasattr(choice.logprobs, "content") and choice.logprobs.content:
                    content_logprobs = choice.logprobs.content
                    for token_logprob in content_logprobs:
                        if hasattr(token_logprob, "token") and hasattr(
                            token_logprob, "logprob"
                        ):
                            token = token_logprob.token
                            logprob = token_logprob.logprob
                            logprobs_dict[token] = logprob

                # Try Together AI format (tokens, token_logprobs)
                elif hasattr(choice.logprobs, "tokens") and hasattr(
                    choice.logprobs, "token_logprobs"
                ):
                    tokens = choice.logprobs.tokens
                    token_logprobs = choice.logprobs.token_logprobs

                    for token, logprob in zip(tokens, token_logprobs):
                        if token is not None and logprob is not None:
                            logprobs_dict[token] = logprob

        except Exception:
            # Silent fallback - don't print debug info in production
            pass
        return logprobs_dict

    def _build_messages(
        self, query: str, context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build messages list for the chat completion.

        Args:
            query: The user query
            context: Optional context to include

        Returns:
            List of message dictionaries
        """
        messages = []

        if context:
            # Add system message with context
            messages.append(
                {
                    "role": "system",
                    "content": f"Use the following context to answer questions:\n\n{context}",
                }
            )

        # Add user query
        messages.append({"role": "user", "content": query})

        return messages

    def _calculate_cost(self, response) -> float:
        """
        Calculate the cost of the API call.

        Args:
            response: API response with usage information

        Returns:
            Cost in USD
        """
        if not response.usage:
            return 0.0

        # Get model pricing
        input_price, output_price = self.MODEL_PRICING.get(self.model, (0.0, 0.0))

        # Calculate cost per million tokens
        prompt_cost = (response.usage.prompt_tokens / 1_000_000) * input_price
        completion_cost = (response.usage.completion_tokens / 1_000_000) * output_price

        return prompt_cost + completion_cost

    def get_cost_estimate(self, query: str, response: str) -> float:
        """
        Estimate the computational cost of generating the response.

        Args:
            query: Input query
            response: Agent response

        Returns:
            Cost estimate in USD
        """
        # Simple token estimation (rough approximation)
        # In practice, actual tokenization would be more accurate
        query_tokens = len(query.split()) * 1.3  # Rough token estimate
        response_tokens = len(response.split()) * 1.3

        input_price, output_price = self.MODEL_PRICING.get(self.model, (0.0, 0.0))

        prompt_cost = (query_tokens / 1_000_000) * input_price
        completion_cost = (response_tokens / 1_000_000) * output_price

        return prompt_cost + completion_cost

    @classmethod
    def get_available_models(cls) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of available model names
        """
        return list(cls.MODEL_PRICING.keys())

    @classmethod
    def get_recommended_models(cls) -> List[Dict[str, str]]:
        """
        Get list of recommended models for Semiosis documentation analysis.

        Returns:
            List of model recommendations with descriptions
        """
        return [
            {
                "name": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
                "description": "Small and efficient serverless model",
                "pricing": "$0.06/1M tokens",
                "use_case": "Quick documentation analysis",
            },
            {
                "name": "Qwen/Qwen2.5-7B-Instruct",
                "description": "Good balance of performance and cost",
                "pricing": "$0.15/1M tokens",
                "use_case": "General text analysis",
            },
            {
                "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
                "description": "Specialized for code and documentation",
                "pricing": "$0.30/1M tokens",
                "use_case": "Code documentation analysis",
            },
            {
                "name": "meta-llama/Llama-3-8B-Instruct-Turbo",
                "description": "Reliable serverless option",
                "pricing": "$0.10/1M tokens",
                "use_case": "Balanced analysis tasks",
            },
        ]

    @classmethod
    def get_model_pricing(cls, model: str) -> Tuple[float, float]:
        """
        Get pricing information for a specific model.

        Args:
            model: Model name

        Returns:
            Tuple of (input_price_per_1M_tokens, output_price_per_1M_tokens)
        """
        return cls.MODEL_PRICING.get(model, (0.0, 0.0))

    @classmethod
    def estimate_monthly_cost(cls, model: str, tokens_per_day: int) -> float:
        """
        Estimate monthly cost for a given usage pattern.

        Args:
            model: Model name
            tokens_per_day: Average tokens processed per day

        Returns:
            Estimated monthly cost in USD
        """
        input_price, output_price = cls.get_model_pricing(model)
        # Assume 50/50 split between input and output tokens
        daily_cost = (tokens_per_day * 0.5 / 1_000_000) * input_price + (
            tokens_per_day * 0.5 / 1_000_000
        ) * output_price
        return daily_cost * 30
