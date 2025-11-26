"""
Mock agent implementation for testing and development.

This module provides a mock agent that can be used when specific agent
implementations are not available.
"""

import time
from typing import Any, Dict, Optional

from semiosis.agents.base import AgentResponse, BaseAgent


class MockAgent(BaseAgent):
    """
    Mock agent implementation for testing and development.

    This agent returns predefined responses to simulate agent behavior
    without requiring actual API calls.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the mock agent.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.response_delay = config.get("response_delay", 0.1)  # seconds
        self.response_template = config.get("response_template", "Response to: {query}")

    def generate_response(
        self, query: str, context: Optional[str] = None
    ) -> AgentResponse:
        """
        Generate a mock response to the given query.

        Args:
            query: The input query to respond to
            context: Optional context to include in the prompt

        Returns:
            AgentResponse containing the output and metadata
        """
        # Simulate processing delay
        time.sleep(self.response_delay)

        # Generate response based on query and context
        if context:
            response_text = f"{self.response_template} with context: {context[:100]}..."
        else:
            response_text = self.response_template.format(query=query)

        # Generate mock logprobs for demonstration
        tokens = response_text.split()
        logprobs = {token: -0.1 * i for i, token in enumerate(tokens, 1)}

        # Calculate mock cost
        cost = self.get_cost_estimate(query, response_text)

        return AgentResponse(
            output=response_text,
            logprobs=logprobs,
            metadata={"model": "mock-agent", "timestamp": time.time()},
            cost=cost,
        )

    def extract_logprobs(
        self, query: str, response: str, context: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Extract token-level log probabilities for the response.

        Args:
            query: The original query
            response: The agent's response
            context: Optional context used in the generation

        Returns:
            Dictionary mapping tokens to their log probabilities
        """
        # Generate mock logprobs based on response content
        tokens = response.split()
        logprobs = {}

        for i, token in enumerate(tokens):
            # Create decreasing probability for later tokens
            logprob = -0.05 * (i + 1)
            logprobs[token] = logprob

        return logprobs
