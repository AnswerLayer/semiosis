"""
Integration tests for Semantic Information Theory engine calculations.
"""

import pytest

from semiosis.agents.base import AgentState
from semiosis.sit.engine import SemioticEvaluator


@pytest.mark.integration
def test_viability_calculation_basic():
    """Test basic viability calculation with known agent states."""
    evaluator = SemioticEvaluator()

    # Add agent states with varying trust and budget levels
    states = [
        AgentState("q1", "a1", trust=0.9, budget=0.05, cost=0.001, parameters={}),
        AgentState("q2", "a2", trust=0.7, budget=0.03, cost=0.002, parameters={}),
        AgentState("q3", "a3", trust=0.5, budget=0.01, cost=0.001, parameters={}),
        AgentState("q4", "a4", trust=0.3, budget=0.0, cost=0.003, parameters={}),
        AgentState("q5", "a5", trust=0.1, budget=-0.01, cost=0.002, parameters={}),
    ]

    for state in states:
        evaluator.add_agent_state(state)

    trust_threshold = 0.6

    # Expected: 2 out of 5 states have trust > 0.6 and budget > 0
    # States 0 (trust=0.9, budget=0.05) and 1 (trust=0.7, budget=0.03)
    viability = evaluator.calculate_viability(trust_threshold)

    assert viability == 0.4  # 2/5 = 0.4


@pytest.mark.integration
def test_viability_calculation_edge_cases():
    """Test viability calculation edge cases."""
    # All viable
    evaluator1 = SemioticEvaluator()
    for i in range(3):
        evaluator1.add_agent_state(
            AgentState(
                f"q{i}", f"a{i}", trust=0.9, budget=0.1, cost=0.001, parameters={}
            )
        )
    assert evaluator1.calculate_viability(0.5) == 1.0

    # None viable (low trust)
    evaluator2 = SemioticEvaluator()
    for i in range(3):
        evaluator2.add_agent_state(
            AgentState(
                f"q{i}", f"a{i}", trust=0.1, budget=0.1, cost=0.001, parameters={}
            )
        )
    assert evaluator2.calculate_viability(0.5) == 0.0

    # None viable (no budget)
    evaluator3 = SemioticEvaluator()
    for i in range(3):
        evaluator3.add_agent_state(
            AgentState(
                f"q{i}", f"a{i}", trust=0.9, budget=-0.1, cost=0.001, parameters={}
            )
        )
    assert evaluator3.calculate_viability(0.5) == 0.0


@pytest.mark.integration
def test_semantic_threshold_calculation():
    """Test semantic threshold calculation with declining trust states."""
    evaluator = SemioticEvaluator()

    # Add states with declining trust to simulate context degradation
    trust_values = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
    for i, trust in enumerate(trust_values):
        evaluator.add_agent_state(
            AgentState(
                f"q{i}", f"a{i}", trust=trust, budget=0.1, cost=0.001, parameters={}
            )
        )

    threshold = evaluator.calculate_semantic_threshold()

    # Threshold should be somewhere in the middle range where viability drops
    # significantly
    assert 0.0 <= threshold <= 1.0


@pytest.mark.integration
def test_trust_update_mechanism():
    """Test trust update based on evaluation results."""
    from semiosis.environments.base import EvaluationResult

    evaluator = SemioticEvaluator()
    initial_trust = 5.0

    # Test correct response increases trust
    correct_result = EvaluationResult(
        success=True, score=0.9, details={"reason": "Good response"}
    )
    new_trust = evaluator.update_trust(initial_trust, correct_result)
    assert new_trust > initial_trust

    # Test incorrect response decreases trust
    incorrect_result = EvaluationResult(
        success=False, score=0.1, details={"reason": "Wrong response"}
    )
    new_trust = evaluator.update_trust(initial_trust, incorrect_result)
    assert new_trust < initial_trust


@pytest.mark.integration
def test_budget_update_mechanism():
    """Test budget update based on cost and trust."""
    evaluator = SemioticEvaluator()
    initial_budget = 10.0
    cost = 1.0
    trust = 5.0

    new_budget = evaluator.update_budget(initial_budget, cost, trust)

    # Budget should be affected by cost and trust
    # With default config: new_budget = budget - cost + (trust * 0.1)
    expected = initial_budget - cost + (trust * 0.1)
    assert abs(new_budget - expected) < 0.01


@pytest.mark.unit
def test_empty_evaluator():
    """Test evaluator behavior with no agent states."""
    evaluator = SemioticEvaluator()

    # Should handle empty state gracefully
    assert evaluator.calculate_viability(0.5) == 0.0
    assert evaluator.calculate_semantic_threshold() == 0.0


@pytest.mark.unit
def test_performance_trajectory():
    """Test performance trajectory extraction."""
    evaluator = SemioticEvaluator()

    # Add a few states
    for i in range(3):
        state = AgentState(
            f"q{i}",
            f"a{i}",
            trust=float(i),
            budget=float(i * 2),
            cost=float(i * 0.1),
            parameters={},
        )
        evaluator.add_agent_state(state)

    trajectory = evaluator.get_performance_trajectory()

    assert "trust" in trajectory
    assert "budget" in trajectory
    assert "cost" in trajectory
    assert len(trajectory["trust"]) == 3
    assert trajectory["trust"] == [0.0, 1.0, 2.0]
