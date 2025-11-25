#!/usr/bin/env python3
"""
Debug script to investigate empty output issue with OllamaAgent.
"""

import sys
import json
import requests
sys.path.insert(0, '.')

from semiosis.agents.ollama_agent import OllamaAgent


def test_raw_ollama_api():
    """Test raw Ollama API to see what's happening."""
    print("=== Testing Raw Ollama API ===")
    
    base_url = "http://localhost:11434"
    
    # Test basic connectivity
    try:
        response = requests.get(f"{base_url}/api/version", timeout=5)
        print(f"✓ Ollama version check: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Version check failed: {e}")
        return False
    
    # Test model list
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=10)
        models_data = response.json()
        print(f"✓ Models available: {len(models_data.get('models', []))}")
        for model in models_data.get('models', []):
            print(f"  - {model['name']}")
    except Exception as e:
        print(f"✗ Models check failed: {e}")
        return False
    
    # Test simple generation
    try:
        payload = {
            "model": "gpt-oss:20b",
            "prompt": "Say hello",
            "stream": False
        }
        
        print(f"\nTesting simple generation:")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{base_url}/api/generate",
            json=payload,
            timeout=30  # Longer timeout for generation
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Raw response keys: {list(result.keys())}")
            print(f"Response content: {json.dumps(result, indent=2)}")
            
            # Check specific fields
            print(f"\nField analysis:")
            print(f"  'response' field: '{result.get('response', 'NOT_FOUND')}'")
            print(f"  'done' field: {result.get('done', 'NOT_FOUND')}")
            print(f"  'total_duration': {result.get('total_duration', 'NOT_FOUND')}")
            
        else:
            print(f"Error response: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"✗ Generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_with_debug():
    """Test OllamaAgent with debug output."""
    print("\n=== Testing OllamaAgent with Debug ===")
    
    try:
        config = {'model': 'gpt-oss:20b', 'temperature': 0.1}
        agent = OllamaAgent(config)
        
        # Monkey patch to add debug output
        original_extract_logprobs = agent._extract_logprobs
        
        def debug_extract_logprobs(result):
            print(f"Debug: _extract_logprobs input keys: {list(result.keys())}")
            print(f"Debug: response field value: '{result.get('response', 'NOT_FOUND')}'")
            print(f"Debug: logprobs field: {result.get('logprobs', 'NOT_FOUND')}")
            return original_extract_logprobs(result)
        
        agent._extract_logprobs = debug_extract_logprobs
        
        print(f"Generating response with agent...")
        response = agent.generate_response('Say hello')
        
        print(f"Agent response:")
        print(f"  Output: '{response.output}' (length: {len(response.output)})")
        print(f"  Logprobs: {response.logprobs}")
        print(f"  Metadata: {response.metadata}")
        
        return True
        
    except Exception as e:
        print(f"✗ Agent debug test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run debug tests."""
    print("Debugging OllamaAgent Empty Output Issue\n")
    
    # Test raw API first
    api_ok = test_raw_ollama_api()
    
    if api_ok:
        # Test agent with debugging
        test_agent_with_debug()
    else:
        print("Skipping agent test due to API issues")


if __name__ == "__main__":
    main()