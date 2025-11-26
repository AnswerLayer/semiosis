"""
Base classes for agent system.

This module defines the fundamental abstract base classes for the Agent system
that will support various LLM providers and logprobs extraction for semantic
information calculations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentResponse:
    """
    Represents a response from an agent with additional metadata.

    Attributes:
        output: The main text output from the agent
        logprobs: Token-level log probabilities if available
        metadata: Additional metadata about the response
        cost: Estimated cost of generating this response
    """

    output: str
    logprobs: Optional[Dict[str, float]] = None  # token -> logprob mapping
    metadata: Optional[Dict[str, Any]] = None
    cost: float = 0.0


@dataclass
class AgentState:
    """
    Represents the state of an agent during evaluation.

    Based on the mathematical framework: a = (q, y, ℓ, c, b, θ)

    Attributes:
        query: Current query/task (q)
        output: Agent's response (y)
        trust: Accumulated trust/likelihood (ℓ)
        cost: Computational cost so far (c)
        budget: Remaining computational budget (b)
        parameters: Model configuration (θ)
    """

    query: str
    output: str
    trust: float
    cost: float
    budget: float
    parameters: Dict[str, Any]


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Semiosis framework.

    This class provides the core interface for different LLM providers and
    ensures consistent response format with logprob support for semantic
    information calculations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the agent with configuration.

        Args:
            config: Configuration dictionary containing agent-specific parameters
                   such as model name, API key, etc.
        """
        self.config = config

    @abstractmethod
    def generate_response(
        self, query: str, context: Optional[str] = None
    ) -> AgentResponse:
        """
        Generate a response to the given query.

        Args:
            query: The input query to respond to
            context: Optional context to include in the prompt

        Returns:
            AgentResponse containing the output and metadata
        """
        pass

    @abstractmethod
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
        pass

    def get_cost_estimate(self, query: str, response: str) -> float:
        """
        Estimate the computational cost of generating the response.

        Args:
            query: Input query
            response: Agent response

        Returns:
            Estimated cost (implementation dependent)
        """
        # Default implementation based on token count
        # Subclasses should override with provider-specific costing
        query_tokens = len(query.split())
        response_tokens = len(response.split())
        return (
            float(query_tokens + response_tokens) * 0.000001
        )  # Placeholder cost per token


class CostEstimator(ABC):
    """
    Abstract base class for estimating computational costs.

    Different agents may have different cost calculation methods
    based on their underlying technology and pricing models.
    """

    @abstractmethod
    def estimate_input_cost(self, query: str) -> float:
        """
        Estimate cost for processing the input query.

        Args:
            query: Input query to process

        Returns:
            Estimated cost
        """
        pass

    @abstractmethod
    def estimate_output_cost(self, response: str) -> float:
        """
        Estimate cost for generating the response.

        Args:
            response: Output response to generate

        Returns:
            Estimated cost
        """
        pass

    def estimate_total_cost(self, query: str, response: str) -> float:
        """
        Estimate total cost for processing query and generating response.

        Args:
            query: Input query
            response: Output response

        Returns:
            Total estimated cost
        """
        return self.estimate_input_cost(query) + self.estimate_output_cost(response)
