#!/usr/bin/env python3
import requests
import json

# Test raw Ollama API call
payload = {
    "model": "gpt-oss:20b",
    "prompt": "Say hello",
    "stream": False,
    "options": {
        "temperature": 0.1,
        "num_predict": 50  # Limit tokens for quick test
    }
}

print("Making raw API call...")
response = requests.post(
    "http://localhost:11434/api/generate",
    json=payload,
    timeout=30
)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"Response keys: {list(result.keys())}")
    print(f"Response field: '{result.get('response', 'MISSING')}'")
    print(f"Done: {result.get('done')}")
    print(f"Full result: {json.dumps(result, indent=2)}")
else:
    print(f"Error: {response.text}")