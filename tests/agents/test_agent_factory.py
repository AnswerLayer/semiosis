#!/usr/bin/env python3
"""
Test agent factory integration.
"""

import sys
import os
import pytest
sys.path.insert(0, '../../')

from semiosis.cli.factories import create_agent
from semiosis.agents.together_agent import TogetherAgent
from semiosis.agents.ollama_agent import OllamaAgent


class TestAgentFactory:
    """Test the agent factory functionality."""
    
    def test_create_together_agent(self):
        """Test creating Together AI agent via factory."""
        if not os.getenv('TOGETHER_API_KEY'):
            pytest.skip("TOGETHER_API_KEY not set")
            
        config = {
            'type': 'together',
            'args': {'model': 'meta-llama/Llama-3.1-8B-Instruct-Turbo'}
        }
        
        agent = create_agent(config)
        assert isinstance(agent, TogetherAgent)
        assert agent.model == 'meta-llama/Llama-3.1-8B-Instruct-Turbo'
    
    def test_create_hosted_agent_alias(self):
        """Test creating hosted agent (alias for Together AI)."""
        if not os.getenv('TOGETHER_API_KEY'):
            pytest.skip("TOGETHER_API_KEY not set")
            
        config = {
            'type': 'hosted',
            'args': {'model': 'mistralai/Mistral-7B-Instruct-v0.2'}
        }
        
        agent = create_agent(config)
        assert isinstance(agent, TogetherAgent)
        assert agent.model == 'mistralai/Mistral-7B-Instruct-v0.2'
    
    def test_create_ollama_agent(self):
        """Test creating Ollama agent via factory."""
        config = {
            'type': 'ollama',
            'args': {'model': 'test-model', 'base_url': 'http://test:11434'}
        }
        
        try:
            agent = create_agent(config)
            # Will fail on validation but should create OllamaAgent instance
            assert False, "Should have failed validation"
        except (ConnectionError, ValueError):
            # Expected - validation should fail for test model
            pass
    
    def test_create_local_agent_alias(self):
        """Test creating local agent (alias for Ollama)."""
        config = {
            'type': 'local', 
            'args': {'model': 'test-model', 'base_url': 'http://test:11434'}
        }
        
        try:
            agent = create_agent(config)
            assert False, "Should have failed validation"
        except (ConnectionError, ValueError):
            # Expected - validation should fail for test model
            pass


if __name__ == "__main__":
    import unittest
    
    # Convert to unittest for standalone running
    suite = unittest.TestSuite()
    
    test_case = TestAgentFactory()
    
    # Add tests that don't require API keys
    suite.addTest(unittest.FunctionTestCase(test_case.test_create_ollama_agent))
    suite.addTest(unittest.FunctionTestCase(test_case.test_create_local_agent_alias))
    
    # Add API-dependent tests if key is available
    if os.getenv('TOGETHER_API_KEY'):
        suite.addTest(unittest.FunctionTestCase(test_case.test_create_together_agent))
        suite.addTest(unittest.FunctionTestCase(test_case.test_create_hosted_agent_alias))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("✅ All factory tests passed!")
    else:
        print("❌ Some factory tests failed.")