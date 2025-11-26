"""
Pytest configuration and shared fixtures for semiosis tests.
"""

from typing import Any, Dict

import pytest

from semiosis.agents.mock_agent import MockAgent
from semiosis.contexts.mock_context import MockContextSystem
from semiosis.environments.mock_environment import MockEnvironment


@pytest.fixture
def mock_agent() -> MockAgent:
    """Create a mock agent for testing."""
    return MockAgent({})


@pytest.fixture
def mock_environment() -> MockEnvironment:
    """Create a mock environment for testing."""
    return MockEnvironment({})


@pytest.fixture
def mock_context() -> MockContextSystem:
    """Create a mock context for testing."""
    return MockContextSystem({})


@pytest.fixture
def sample_query() -> str:
    """Sample query for testing."""
    return "What is the average salary by department?"


@pytest.fixture
def sample_agent_state() -> Dict[str, Any]:
    """Sample agent state for SIT testing."""
    return {
        "query": "What is the average salary by department?",
        "output": "SELECT department, AVG(salary) FROM employees GROUP BY department",
        "trust": 0.8,
        "cost": 0.001,
        "budget": 0.1,
        "parameters": {"model": "test-model", "temperature": 0.0},
    }


@pytest.fixture
def sample_evaluation_states() -> list:
    """Sample evaluation states for viability testing."""
    return [
        {"trust": 0.9, "budget": 0.05, "cost": 0.001},
        {"trust": 0.7, "budget": 0.03, "cost": 0.002},
        {"trust": 0.5, "budget": 0.01, "cost": 0.001},
        {"trust": 0.3, "budget": 0.0, "cost": 0.003},
        {"trust": 0.1, "budget": -0.01, "cost": 0.002},
    ]
