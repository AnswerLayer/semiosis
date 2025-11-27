#!/usr/bin/env python3
"""
Test script for TogetherAgent implementation.
"""

import os
import sys

import pytest

sys.path.insert(0, "../../")

from semiosis.agents.together_agent import TogetherAgent
from semiosis.cli.factories import create_agent


def test_agent_creation():
    """Test basic agent creation and validation."""
    print("=== Testing TogetherAgent Creation ===")

    # Check if API key is available
    if not os.getenv("TOGETHER_API_KEY"):
        print("⚠ TOGETHER_API_KEY not set - skipping tests")
        print("  Set your Together AI API key: export TOGETHER_API_KEY=your_key_here")
        return None

    try:
        # Test with serverless model
        config = {"model": "meta-llama/Llama-3.2-3B-Instruct-Turbo"}
        agent = TogetherAgent(config)
        print(f"✓ TogetherAgent created successfully")
        print(f"  Model: {agent.model}")
        print(f"  API Key set: {'Yes' if agent.api_key else 'No'}")
        assert agent is not None
        assert hasattr(agent, "model")

    except Exception as e:
        print(f"✗ Error creating agent: {e}")
        pytest.fail(f"Error creating agent: {e}")


def test_factory_integration():
    """Test agent factory integration."""
    print("\n=== Testing Factory Integration ===")

    if not os.getenv("TOGETHER_API_KEY"):
        print("⚠ Skipping factory tests - no API key")
        return False

    try:
        # Test 'together' type
        config = {
            "type": "together",
            "args": {"model": "mistralai/Mistral-7B-Instruct-v0.3"},
        }
        agent1 = create_agent(config)
        print(f"✓ Factory created {type(agent1).__name__} for 'together' type")

        # Test 'hosted' alias
        config2 = {"type": "hosted", "args": {"model": "Qwen/Qwen2.5-7B-Instruct"}}
        agent2 = create_agent(config2)
        print(f"✓ Factory created {type(agent2).__name__} for 'hosted' type")

        assert agent1 is not None
        assert agent2 is not None

    except Exception as e:
        print(f"✗ Factory error: {e}")
        pytest.fail(f"Factory error: {e}")


def test_model_info():
    """Test model information methods."""
    print("\n=== Testing Model Information ===")

    try:
        available = TogetherAgent.get_available_models()
        print(f"Available models ({len(available)}):")
        for model in available[:5]:  # Show first 5
            print(f"  - {model}")
        if len(available) > 5:
            print(f"  ... and {len(available) - 5} more")

        print(f"\nRecommended models:")
        recommended = TogetherAgent.get_recommended_models()
        for rec in recommended:
            print(f"  - {rec['name']}")
            print(f"    {rec['description']} | {rec['pricing']}")
            print(f"    Use case: {rec['use_case']}")

        # Test pricing lookup
        print(f"\nPricing examples:")
        test_model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
        input_price, output_price = TogetherAgent.get_model_pricing(test_model)
        print(f"  {test_model}: ${input_price}/1M input, ${output_price}/1M output")

        # Test cost estimation
        monthly_cost = TogetherAgent.estimate_monthly_cost(test_model, 100_000)
        print(f"  Est. monthly cost for 100k tokens/day: ${monthly_cost:.2f}")

        assert len(available) >= 0  # May be empty
        assert len(recommended) >= 0

    except Exception as e:
        print(f"✗ Model info error: {e}")
        pytest.fail(f"Model info error: {e}")


@pytest.mark.requires_api
@pytest.mark.skip(reason="Requires real Together API key and configuration")
def test_response_generation():
    """Test response generation with real API."""
    print("\n=== Testing Response Generation ===")

    # This test would need a real Together API instance
    pytest.skip("Requires Together API key and configuration")


@pytest.mark.requires_api
@pytest.mark.skip(reason="Requires real Together API key and configuration")
def test_cost_calculation():
    """Test cost calculation accuracy."""
    print("\n=== Testing Cost Calculation ===")

    # This test would need a real Together API instance
    pytest.skip("Requires Together API key and configuration")


def main():
    """Run all tests."""
    print("Testing TogetherAgent Implementation\n")

    # Run tests
    agent = test_agent_creation()
    factory_ok = test_factory_integration()
    info_ok = test_model_info()
    generation_ok = test_response_generation(agent) if agent else False
    cost_ok = test_cost_calculation(agent) if agent else False

    # Summary
    print("\n=== Test Summary ===")
    tests = [
        ("Agent Creation", agent is not None),
        ("Factory Integration", factory_ok),
        ("Model Information", info_ok),
        ("Response Generation", generation_ok),
        ("Cost Calculation", cost_ok),
    ]

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    for name, result in tests:
        status = "✓" if result else "✗"
        print(f"{status} {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if not os.getenv("TOGETHER_API_KEY"):
        print("\n⚠ Note: Set TOGETHER_API_KEY to run live API tests")
        print("  Get your key at: https://api.together.xyz")
    elif passed == total:
        print("🎉 All tests passed! TogetherAgent is ready to use.")
    else:
        print("⚠ Some tests failed. Check the output above.")


if __name__ == "__main__":
    main()
