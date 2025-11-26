"""
Semantic Information Theory engine.

This module implements the core mathematical framework for semantic information
theory calculations, including trust/budget dynamics and viability measurements.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import numpy as np

from semiosis.agents.base import AgentState
from semiosis.environments.base import EvaluationResult


@dataclass
class TrustConfig:
    """
    Configuration for trust update functions.

    Attributes:
        update_function: Function to update trust based on log-likelihood
        min_trust: Minimum allowed trust value
        max_trust: Maximum allowed trust value
        default_logprob: Default logprob value for missing tokens
    """

    update_function: Optional[Callable[[float], float]] = None
    min_trust: float = 0.0
    max_trust: float = 100.0
    default_logprob: float = -10.0  # Default for missing token probabilities

    def __post_init__(self):
        if self.update_function is None:
            # Default trust update function: add normalized log-likelihood
            self.update_function = lambda ll: ll * 10.0


@dataclass
class BudgetConfig:
    """
    Configuration for budget update functions.

    Attributes:
        cost_function: Function to calculate cost from agent actions
        update_function: Function to update budget based on trust and costs
        initial_budget: Starting budget for agents
        min_budget: Minimum allowed budget (viability threshold)
    """

    cost_function: Optional[Callable[[str, str], float]] = None
    update_function: Optional[Callable[[float, float, float], float]] = None
    initial_budget: float = 100.0
    min_budget: float = 0.0

    def __post_init__(self):
        if self.cost_function is None:
            # Default cost function: length-based approximation
            self.cost_function = lambda query, response: len(query) + len(response)
        if self.update_function is None:
            # Default budget update: budget decreases by cost, increases with trust
            self.update_function = (
                lambda budget, cost, trust: budget - cost + (trust * 0.1)
            )


class SemioticEvaluator:
    """
    Core evaluator for semantic information theory calculations.

    Implements the mathematical framework:
    - V(η) = Pr(ℓ > ℓ_min ∧ b > 0) (Viability function)
    - η_c = inf{η | V(η) ≤ ½V(1)} (Semantic threshold)
    """

    def __init__(
        self,
        trust_config: Optional[TrustConfig] = None,
        budget_config: Optional[BudgetConfig] = None,
    ):
        """
        Initialize the semiotic evaluator.

        Args:
            trust_config: Configuration for trust dynamics
            budget_config: Configuration for budget dynamics
        """
        self.trust_config = trust_config or TrustConfig()
        self.budget_config = budget_config or BudgetConfig()
        self.agent_states: List[AgentState] = []

    def add_agent_state(self, state: AgentState):
        """
        Add an agent state to the evaluation trace.

        Args:
            state: Agent state to add
        """
        self.agent_states.append(state)

    def calculate_log_likelihood(
        self, token_probs: Dict[str, float], target_sequence: str
    ) -> float:
        """
        Calculate log-likelihood from token probabilities.

        Args:
            token_probs: Dictionary mapping tokens to log probabilities
            target_sequence: Target sequence to calculate likelihood for

        Returns:
            Log-likelihood of the target sequence
        """
        # Split target into tokens (simplified - in practice would use proper
        # tokenization)
        tokens = target_sequence.split()

        log_likelihood = 0.0
        for token in tokens:
            if token in token_probs:
                log_likelihood += token_probs[token]
            else:
                # Use default logprob for missing tokens
                log_likelihood += self.trust_config.default_logprob

        return log_likelihood

    def update_trust(
        self, current_trust: float, evaluation_result: EvaluationResult
    ) -> float:
        """
        Update trust based on evaluation feedback from environment.

        Trust reflects agent alignment with the environment rather than
        internal model confidence. High trust means the agent consistently
        produces correct responses given the available context.

        Args:
            current_trust: Current trust value
            evaluation_result: EvaluationResult from environment evaluation

        Returns:
            Updated trust value
        """
        if evaluation_result.correct:
            # Reward correct responses - proportional to score quality
            trust_delta = evaluation_result.score * 2.0
        else:
            # Penalize incorrect responses
            trust_delta = -1.0

        new_trust = current_trust + trust_delta

        # Apply bounds
        new_trust = max(
            self.trust_config.min_trust, min(new_trust, self.trust_config.max_trust)
        )

        return new_trust

    def update_budget(self, current_budget: float, cost: float, trust: float) -> float:
        """
        Update budget based on cost and current trust.

        Args:
            current_budget: Current budget value
            cost: Cost of agent action
            trust: Current trust value

        Returns:
            Updated budget value
        """
        new_budget = self.budget_config.update_function(current_budget, cost, trust)

        # Apply bounds
        new_budget = max(self.budget_config.min_budget, new_budget)

        return new_budget

    def calculate_viability(
        self, trust_threshold: float, budget_threshold: Optional[float] = None
    ) -> float:
        """
        Calculate viability: V(η) = Pr(ℓ > ℓ_min ∧ b > 0).

        Args:
            trust_threshold: Minimum trust threshold (ℓ_min)
            budget_threshold: Minimum budget threshold (defaults to min_budget)

        Returns:
            Viability value between 0 and 1
        """
        if not self.agent_states:
            return 0.0

        budget_thresh = budget_threshold or self.budget_config.min_budget

        # Count states where trust > threshold AND budget > 0
        viable_states = [
            state
            for state in self.agent_states
            if state.trust > trust_threshold and state.budget > budget_thresh
        ]

        return len(viable_states) / len(self.agent_states)

    def calculate_semantic_threshold(self) -> float:
        """
        Calculate semantic threshold: η_c = inf{η | V(η) ≤ ½V(1)}.

        Returns:
            Semantic threshold value
        """
        if not self.agent_states:
            return 0.0

        # Calculate V(1) - viability with minimal trust threshold
        max_viability = self.calculate_viability(
            trust_threshold=0.0
        )  # Any positive threshold

        # Target viability is half of maximum viability
        target_viability = 0.5 * max_viability

        # Binary search for the threshold where viability drops to target
        low, high = 0.0, max(state.trust for state in self.agent_states)

        for _ in range(50):  # Limit iterations
            mid = (low + high) / 2
            mid_viability = self.calculate_viability(mid)

            if mid_viability <= target_viability:
                high = mid
            else:
                low = mid

        return low

    def calculate_mutual_information(
        self, agent_states: List[AgentState], environment_states: List[Any]
    ) -> float:
        """
        Calculate mutual information between agent and environment: I(A:E).

        Args:
            agent_states: List of agent states
            environment_states: List of environment states

        Returns:
            Mutual information value
        """
        # This is a simplified implementation
        # In practice, this would involve more complex probability calculations
        if len(agent_states) != len(environment_states) or not agent_states:
            return 0.0

        # Calculate entropy of agent states
        agent_trust_values = [state.trust for state in agent_states]
        agent_entropy = self._calculate_entropy(agent_trust_values)

        # Calculate entropy of environment states
        # For simplicity, we'll use the distribution of some environment metric
        env_entropy = self._calculate_entropy(
            [hash(str(e)) % 1000 for e in environment_states]
        )

        # Approximate mutual information (this is a simplified approach)
        # In reality, this would require joint probability distributions
        return (agent_entropy + env_entropy) / 2.0

    def _calculate_entropy(self, values: List[float]) -> float:
        """
        Calculate the entropy of a set of values.

        Args:
            values: List of values to calculate entropy for

        Returns:
            Entropy value
        """
        if not values:
            return 0.0

        # Convert to probability distribution
        values_array = np.array(values)
        values_array = np.abs(values_array)  # Ensure non-negative for probability
        if np.sum(values_array) == 0:
            return 0.0

        probs = values_array / np.sum(values_array)
        probs = probs[probs > 0]  # Remove zero probabilities

        # Calculate entropy
        return -np.sum(probs * np.log2(probs))

    def get_performance_trajectory(self) -> Dict[str, List[float]]:
        """
        Get the performance trajectory of the agent over time.

        Returns:
            Dictionary with lists of values for trust, budget, and cost over time
        """
        if not self.agent_states:
            return {"trust": [], "budget": [], "cost": []}

        return {
            "trust": [state.trust for state in self.agent_states],
            "budget": [state.budget for state in self.agent_states],
            "cost": [state.cost for state in self.agent_states],
        }
