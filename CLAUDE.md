# CLAUDE.md

This file provides guidance to Claude Code when working with the Semiosis repository.

## Project Overview

Semiosis is an open-source command-line tool for evaluating LLM agents using Semantic Information Theory (SIT). The framework measures agent viability through trust and budget dynamics rather than simple accuracy metrics.

## GitHub Integration

This repository uses **GitHub Issues** for task management and community coordination.

### Issue Management Workflow

1. **Creating Issues**: Use GitHub issues for all feature requests, bugs, and tasks
2. **Branch Naming**: Use descriptive names like `feature/agent-abstraction` or `fix/logprob-extraction`
3. **Commit References**: Use `#issue-number` to reference GitHub issues in commits
4. **Pull Requests**: Always reference the related issue with `Closes #XXX` or `Fixes #XXX`

## Architecture Overview

### Core Components

```
semiosis/
├── agents/          # Agent implementations (OpenAI, Anthropic, local models)
├── environments/    # Evaluation environments (text-to-SQL, code-gen, custom)
├── contexts/        # Context system integrations (DBT, GraphRAG, MCP)
├── interventions/   # Context modification strategies
├── sit/            # Semantic Information Theory engine
├── cli/            # Command-line interface
├── evaluation/     # Evaluation orchestration
├── visualization/  # Results visualization and reporting
└── plugins/        # Plugin system for extensibility
```

### Key Design Principles

1. **Environment-Centric**: Everything revolves around Environment abstraction
2. **Modular**: Each component is independently testable and extensible
3. **Community-Driven**: Plugin architecture for community contributions
4. **Research-Focused**: Built to validate and extend SIT theory

## Development Commands

### Setup and Installation
```bash
cd semiosis
pip install -e ".[dev]"          # Install in development mode
pre-commit install               # Install pre-commit hooks
```

### Testing
```bash
pytest                          # Run all tests
pytest tests/unit/              # Run unit tests only
pytest tests/integration/       # Run integration tests
pytest --cov=semiosis          # Run with coverage
pytest -m "not slow"           # Skip slow tests
pytest -m "not requires_api"   # Skip tests requiring API keys
```

### Code Quality
```bash
black semiosis/ tests/          # Format code
isort semiosis/ tests/          # Sort imports
flake8 semiosis/ tests/         # Lint code
mypy semiosis/                  # Type checking
```

### Running Evaluations
```bash
# Basic text-to-SQL evaluation
semiosis evaluate \
    --agent openai \
    --agent-args model=gpt-4 \
    --environment text-to-sql \
    --environment-args task_source=spider2 \
    --context dbt \
    --context-args project_path=./dbt_project

# Custom environment evaluation  
semiosis evaluate \
    --environment custom \
    --environment-args config_file=./my_env.yaml \
    --agent anthropic \
    --interventions noise.add_random,context.remove_elements
```

## Mathematical Foundation

The framework implements Semantic Information Theory calculations:

```python
# Agent State
@dataclass
class AgentState:
    query: str              # q - current query/task
    output: str             # y - agent's response  
    trust: float            # ℓ - accumulated trust
    cost: float             # c - computational cost
    budget: float           # b - remaining resources
    parameters: dict        # θ - model config

# Core SIT Calculations
def calculate_viability(states: List[AgentState], 
                       trust_threshold: float) -> float:
    """V(η) = Pr(ℓ > ℓ_min ∧ b > 0)"""
    viable = [s for s in states if s.trust > trust_threshold and s.budget > 0]
    return len(viable) / len(states)

def find_semantic_threshold(viability_curve: List[Tuple[float, float]]) -> float:
    """η_c = inf{η | V(η) ≤ ½V(1)}"""
    baseline_viability = viability_curve[0][1]  # V(1) - no context
    threshold_target = 0.5 * baseline_viability
    
    for noise_level, viability in viability_curve:
        if viability <= threshold_target:
            return noise_level
    return float('inf')
```

## Testing Guidelines

### Test Categories
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete evaluation workflows

### API Key Management
- Mark tests requiring API keys with `@pytest.mark.requires_api`
- Tests should gracefully skip if keys are unavailable
- Use environment variables for API key configuration
- Never commit API keys to the repository

### Mock Usage
- Mock external API calls in unit tests
- Use real APIs sparingly in integration tests with rate limiting
- Provide fixture data for reproducible tests

## Community Guidelines

### Code Style
- **Line length**: 88 characters (Black default)
- **Type hints**: Comprehensive typing throughout
- **Docstrings**: Google-style docstrings for all public methods
- **Imports**: isort with black profile

### Contribution Workflow
1. **Find or create GitHub issue** for the work
2. **Fork and create feature branch** with descriptive name
3. **Implement with tests** ensuring coverage
4. **Run quality checks** (black, isort, flake8, mypy, pytest)
5. **Create pull request** referencing the GitHub issue
6. **Address review feedback** and merge when approved

### Breaking Changes
- Avoid breaking changes in minor versions
- Document migration paths for major version changes
- Use deprecation warnings before removing functionality
- Maintain backward compatibility where possible

## Research Context

### Theoretical Foundation
Based on Sowinsky et al. 2023 "Semantic Information in a model of Resource Gathering Agents" - applying biological viability concepts to AI agent evaluation.

### Key Innovations
- **Viability-based evaluation** instead of accuracy-only metrics
- **Trust and budget dynamics** for sustainable agent operation
- **Semantic threshold detection** for critical information boundaries
- **Context intervention analysis** for robustness measurement

### Academic Applications
- Context optimization for production deployment
- Agent robustness analysis under information constraints
- Resource planning for sustained AI system operation
- Comparative evaluation beyond traditional benchmarks

## Security Considerations

### API Key Management
- Store API keys in environment variables only
- Use `.env` files for local development (git-ignored)

### Code Execution Security
- Sandbox SQL execution in isolated environments
- Validate all user inputs and configurations
- Implement timeouts for long-running operations
- Use parameterized queries to prevent SQL injection

### Plugin Security
- Validate plugin interfaces and implementations
- Implement proper isolation between plugins
- Review community plugins before inclusion
- Provide security guidelines for plugin developers

## Performance Guidelines

### Evaluation Performance
- Cache expensive operations (manifest parsing, model loading)
- Support parallel execution where possible
- Implement progress reporting for long evaluations
- Optimize database queries and result processing

### Memory Management
- Stream large datasets instead of loading entirely
- Clean up temporary files and resources
- Monitor memory usage in long-running evaluations
- Implement configurable batch sizes for processing

## Important Reminders

1. **No Linear References**: This is an open-source project - use GitHub issues only
2. **Community First**: Design for community adoption and contribution
3. **Research Focus**: Maintain scientific rigor and theoretical grounding
4. **Quality Standards**: Comprehensive testing and documentation required
5. **Security Awareness**: Handle API keys and user inputs safely
6. **Performance Conscious**: Design for efficiency at scale

## Quick Reference

### Common Tasks
- Create issue: Use GitHub issues for any work item
- Start feature: `git checkout -b feature/descriptive-name`
- Run tests: `pytest` (with coverage: `pytest --cov=semiosis`)
- Check quality: `black . && isort . && flake8 . && mypy semiosis/`
- Submit PR: Reference GitHub issue with `Closes #XXX`

### File Conventions
- Test files: `test_*.py` in `tests/` directory
- Type hints: Required for all public interfaces
- Docstrings: Google-style for all classes and functions
- Configuration: YAML preferred, with schema validation

This repository represents a novel approach to AI agent evaluation - help build something the community will value! 🚀