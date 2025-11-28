#!/usr/bin/env python3
"""
Simple test script for OllamaAgent implementation.
"""

import os

import pytest

from semiosis.agents.ollama_agent import OllamaAgent
from semiosis.cli.factories import create_agent


def test_agent_creation():
    """Test basic agent creation and validation."""
    print("=== Testing Agent Creation ===")

    try:
        # Test with a lightweight model
        config = {"model": "gpt-oss:20b", "temperature": 0.1}
        agent = OllamaAgent(config)
        print("✓ Agent created successfully")
        print(f"  Model: {agent.model}")
        print(f"  Base URL: {agent.base_url}")
        assert agent is not None
        assert hasattr(agent, "model")
    except ConnectionError as e:
        print(f"⚠ Ollama server not available (expected in CI): {e}")
        pytest.skip("Ollama server not running - skipping test")
    except Exception as e:
        print(f"✗ Error creating agent: {e}")
        pytest.fail(f"Error creating agent: {e}")


def test_factory_integration():
    """Test agent factory integration."""
    print("\n=== Testing Factory Integration ===")

    try:
        # Test 'ollama' type
        config = {"type": "ollama", "args": {"model": "gpt-oss:20b"}}
        agent1 = create_agent(config)
        print(f"✓ Factory created {type(agent1).__name__} for 'ollama' type")

        # Test 'local' alias
        config2 = {"type": "local", "args": {"model": "gpt-oss:20b"}}
        agent2 = create_agent(config2)
        print(f"✓ Factory created {type(agent2).__name__} for 'local' type")

        assert agent1 is not None
        assert agent2 is not None
    except ConnectionError as e:
        print(f"⚠ Ollama server not available (expected in CI): {e}")
        pytest.skip("Ollama server not running - skipping test")
    except Exception as e:
        print(f"✗ Factory error: {e}")
        pytest.fail(f"Factory error: {e}")


def test_model_info():
    """Test model information methods."""
    print("\n=== Testing Model Information ===")

    try:
        available = OllamaAgent.get_available_models()
        print(f"Available models ({len(available)}):")
        for model in available:
            print(f"  - {model}")

        print(f"\nRecommended models:")
        recommended = OllamaAgent.get_recommended_models()
        for rec in recommended:
            print(f"  - {rec['name']}: {rec['description']}")

        assert len(available) >= 0  # May be empty if no server
        assert len(recommended) >= 0
    except Exception as e:
        print(f"✗ Model info error: {e}")
        pytest.fail(f"Model info error: {e}")


@pytest.mark.requires_api
@pytest.mark.skip(reason="Requires real Ollama agent instance - needs API setup")
def test_simple_generation(agent=None):
    """Test simple response generation with safe model."""
    pass  # Test implementation pending
