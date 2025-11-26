# Semiosis Tests

This directory contains the test suite for the Semiosis framework.

## Test Organization

```
tests/
├── agents/                    # Agent implementation tests
│   ├── test_ollama_agent.py   # Local Ollama model tests
│   ├── test_together_agent.py # Together AI hosted model tests
│   └── test_agent_factory.py  # Agent factory integration tests
├── unit/                      # Unit tests for individual components
├── integration/               # Integration tests between components
└── run_tests.py               # Test runner script
```

## Running Tests

### Run All Tests
```bash
cd tests
python3 run_tests.py
```

### Run Specific Test Files
```bash
# Test Ollama agent (requires Ollama running locally)
python3 tests/agents/test_ollama_agent.py

# Test Together AI agent (requires TOGETHER_API_KEY)
python3 tests/agents/test_together_agent.py

# Test agent factory
python3 tests/agents/test_agent_factory.py
```

## Prerequisites

### Required Python Packages
```bash
pip install requests openai
```

### API Keys and Services

**Together AI Tests:**
- Set environment variable: `export TOGETHER_API_KEY=your_key_here`
- Get your key at: https://api.together.xyz

**Ollama Tests:**
- Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
- Start service: `ollama serve`
- Pull a model: `ollama pull sqlcoder:7b`

## Test Categories

### Agent Tests (`tests/agents/`)
- **Unit tests** for individual agent implementations
- **Integration tests** for agent factory and configuration
- **Live API tests** (when credentials available)

### Expected Test Coverage
- Agent creation and configuration validation
- Factory pattern integration 
- Error handling and edge cases
- Cost calculation accuracy
- Logprobs extraction (where supported)
- Model availability and validation

### CI/CD Integration
Tests are designed to:
- Skip live API tests when credentials unavailable
- Provide clear success/failure feedback
- Run quickly for development workflow
- Support both local and CI environments

## Adding New Tests

### For New Agent Types
1. Create `test_<agent_name>_agent.py` in `tests/agents/`
2. Follow the pattern from existing agent tests
3. Add factory integration tests
4. Update this README

### For New Components
1. Create appropriate subdirectory (`unit/`, `integration/`)
2. Follow naming convention: `test_<component>.py`
3. Add to test runner if needed

## Test Output

The test runner provides:
- ✓ Prerequisites check (packages, API keys, services)
- ✓ Individual test file results
- ✓ Comprehensive summary
- ⚠ Clear guidance for missing dependencies
- 🎉 Celebration for full success

Example output:
```
=== Checking Prerequisites ===
✓ requests installed
✓ openai installed
✓ TOGETHER_API_KEY: Set
⚠ Ollama service: Not running

=== Running test_together_agent.py ===
✓ test_together_agent.py passed

=== Test Summary ===
✓ test_together_agent.py
⚠ test_ollama_agent.py

Results: 1/2 tests passed
```