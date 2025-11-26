#!/usr/bin/env python3
"""
Simple test script for OllamaAgent implementation.
"""

import sys
import os
sys.path.insert(0, '../../')

from semiosis.agents.ollama_agent import OllamaAgent
from semiosis.cli.factories import create_agent


def test_agent_creation():
    """Test basic agent creation and validation."""
    print("=== Testing Agent Creation ===")
    
    try:
        # Test with a lightweight model
        config = {'model': 'gpt-oss:20b', 'temperature': 0.1}
        agent = OllamaAgent(config)
        print(f"✓ Agent created successfully")
        print(f"  Model: {agent.model}")
        print(f"  Base URL: {agent.base_url}")
        return agent
    except Exception as e:
        print(f"✗ Error creating agent: {e}")
        return None


def test_factory_integration():
    """Test agent factory integration."""
    print("\n=== Testing Factory Integration ===")
    
    try:
        # Test 'ollama' type
        config = {
            'type': 'ollama',
            'args': {'model': 'gpt-oss:20b'}
        }
        agent1 = create_agent(config)
        print(f"✓ Factory created {type(agent1).__name__} for 'ollama' type")
        
        # Test 'local' alias
        config2 = {
            'type': 'local', 
            'args': {'model': 'gpt-oss:20b'}
        }
        agent2 = create_agent(config2)
        print(f"✓ Factory created {type(agent2).__name__} for 'local' type")
        
        return True
    except Exception as e:
        print(f"✗ Factory error: {e}")
        return False


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
            
        return True
    except Exception as e:
        print(f"✗ Model info error: {e}")
        return False


def test_simple_generation(agent):
    """Test simple response generation with safe model."""
    print("\n=== Testing Response Generation ===")
    
    if not agent:
        print("✗ No agent available for testing")
        return False
        
    try:
        # Use a very simple prompt
        print("Generating response for: 'Hello'")
        response = agent.generate_response('Hello')
        
        print(f"✓ Response generated")
        print(f"  Output length: {len(response.output)} chars")
        print(f"  Cost: ${response.cost}")
        print(f"  Provider: {response.metadata.get('provider')}")
        print(f"  Logprobs available: {response.metadata.get('logprobs_available')}")
        print(f"  Response time: {response.metadata.get('response_time', 0):.2f}s")
        
        if response.output:
            preview = response.output[:100].replace('\n', ' ')
            print(f"  Preview: '{preview}'")
        else:
            print("  ⚠ Empty output (may be normal for some models)")
            
        return True
        
    except Exception as e:
        print(f"✗ Generation error: {e}")
        return False


def main():
    """Run all tests."""
    print("Testing OllamaAgent Implementation\n")
    
    # Run tests
    agent = test_agent_creation()
    factory_ok = test_factory_integration()
    info_ok = test_model_info()
    generation_ok = test_simple_generation(agent)
    
    # Summary
    print("\n=== Test Summary ===")
    tests = [
        ("Agent Creation", agent is not None),
        ("Factory Integration", factory_ok),
        ("Model Information", info_ok),
        ("Response Generation", generation_ok)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
        
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! OllamaAgent is ready to use.")
    else:
        print("⚠ Some tests failed. Check the output above.")


if __name__ == "__main__":
    main()