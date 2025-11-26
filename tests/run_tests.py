#!/usr/bin/env python3
"""
Test runner for Semiosis agent tests.

This script runs all agent tests in the proper order and provides
a comprehensive test report.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_prerequisites():
    """Check if required dependencies are available."""
    print("=== Checking Prerequisites ===")
    
    # Check Python packages
    required_packages = ['requests', 'openai']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} missing")
    
    if missing_packages:
        print(f"\nInstall missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    # Check API keys
    api_keys = {
        'TOGETHER_API_KEY': 'Together AI tests',
        'OLLAMA_AVAILABLE': 'Ollama tests (check if Ollama is running)'
    }
    
    print(f"\nAPI Key Status:")
    together_available = bool(os.getenv('TOGETHER_API_KEY'))
    print(f"{'✓' if together_available else '⚠'} TOGETHER_API_KEY: {'Set' if together_available else 'Not set'}")
    
    # Check if Ollama is running
    try:
        import requests
        response = requests.get('http://localhost:11434/api/version', timeout=2)
        ollama_available = response.status_code == 200
        print(f"{'✓' if ollama_available else '⚠'} Ollama service: {'Running' if ollama_available else 'Not running'}")
    except:
        ollama_available = False
        print("⚠ Ollama service: Not running")
    
    return True


def run_test_file(test_file):
    """Run a specific test file."""
    print(f"\n=== Running {test_file.name} ===")
    
    try:
        result = subprocess.run([
            sys.executable, str(test_file)
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✓ {test_file.name} passed")
            if result.stdout:
                print("Output:", result.stdout.split('\n')[-3])  # Last meaningful line
            return True
        else:
            print(f"✗ {test_file.name} failed")
            if result.stderr:
                print("Error:", result.stderr.split('\n')[0])  # First error line
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {test_file.name} timed out")
        return False
    except Exception as e:
        print(f"✗ {test_file.name} error: {e}")
        return False


def main():
    """Run all tests."""
    print("Semiosis Agent Test Runner\n")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install missing dependencies.")
        return False
    
    # Find all test files
    test_dir = Path(__file__).parent / 'agents'
    test_files = sorted(test_dir.glob('test_*.py'))
    
    if not test_files:
        print("\n⚠ No test files found in tests/agents/")
        return False
    
    print(f"\nFound {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {test_file.name}")
    
    # Run tests
    results = {}
    for test_file in test_files:
        results[test_file.name] = run_test_file(test_file)
    
    # Summary
    print("\n=== Test Summary ===")
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠ Some tests failed. Check output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)