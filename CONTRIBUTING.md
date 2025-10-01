# Contributing to Semiosis

Thank you for your interest in contributing to Semiosis! This document provides guidelines and information for contributors.

## 🎯 Project Vision

Semiosis aims to revolutionize LLM agent evaluation by applying Semantic Information Theory principles. We're building a community-driven framework that enables researchers and practitioners to evaluate agents based on viability and semantic information flow, not just accuracy.

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/semiosis.git
   cd semiosis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests to verify setup**
   ```bash
   pytest tests/
   ```

## 📋 Development Workflow

### GitHub Issues Integration

We use GitHub Issues for project management and community coordination:

1. **Find or create a GitHub issue** for your contribution
2. **Create a branch** using descriptive naming: `your-name/feature-description` or `your-name/fix-description`
3. **Reference the GitHub issue** in commits and pull requests using `#issue-number`

### Branch Naming Convention

- Feature: `your-name/feature-description`
- Bug fix: `your-name/fix-description`  
- Documentation: `your-name/docs-description`

### Commit Messages

Follow [Conventional Commits](https://conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Examples:
```
feat(agents): add Anthropic Claude agent support

Implements AnthropicAgent class with Message API integration
and token probability extraction where available.

Closes #42
```

```
fix(sit): handle zero probabilities in log-likelihood calculation

Prevents math domain errors when tokens have zero probability
by using configurable default log probability value.

Fixes #15
```

## 🏗️ Architecture Guidelines

### Code Organization

```
semiosis/
├── agents/          # Agent implementations
├── environments/    # Environment definitions  
├── contexts/        # Context system integrations
├── interventions/   # Context intervention strategies
├── sit/            # Semantic Information Theory engine
├── cli/            # Command-line interface
├── evaluation/     # Evaluation orchestration
├── visualization/  # Results visualization
└── plugins/        # Plugin system
```

### Design Principles

1. **Modularity**: Each component should be independently testable
2. **Extensibility**: Easy to add new agents, environments, contexts
3. **Type Safety**: Comprehensive type hints throughout
4. **Documentation**: Clear docstrings and examples
5. **Performance**: Efficient for large-scale evaluations

### Abstract Base Classes

All major components inherit from abstract base classes:

- `BaseAgent` - For all agent implementations
- `BaseEnvironment` - For evaluation environments
- `TaskGenerator` - For task creation
- `TaskEvaluator` - For response evaluation
- `BaseContextSystem` - For context integrations
- `BaseIntervention` - For context modifications

## 🧪 Testing

### Test Categories

- **Unit tests** (`tests/unit/`): Test individual components in isolation
- **Integration tests** (`tests/integration/`): Test component interactions
- **End-to-end tests** (`tests/e2e/`): Test complete evaluation workflows

### Test Naming

```python
def test_agent_generates_response_with_logprobs():
    """Test that agent returns logprobs when requested."""
    pass

def test_environment_handles_missing_ground_truth():
    """Test environment gracefully handles tasks without ground truth."""
    pass
```

### Running Tests

```bash
# All tests
pytest

# Specific category
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=semiosis

# Skip slow tests
pytest -m "not slow"

# Skip tests requiring API keys
pytest -m "not requires_api"
```

### API Key Tests

Tests requiring API keys should be marked with `@pytest.mark.requires_api` and should gracefully skip if keys are not available.

## 📝 Documentation

### Docstring Format

Use Google-style docstrings:

```python
def calculate_viability(self, agent_states: List[AgentState], 
                       trust_threshold: float) -> float:
    """Calculate agent viability from state trajectory.
    
    Args:
        agent_states: List of agent states over evaluation
        trust_threshold: Minimum trust level for viability
        
    Returns:
        Viability score between 0.0 and 1.0
        
    Raises:
        ValueError: If agent_states is empty
        
    Example:
        >>> evaluator = SemioticEvaluator(trust_config, budget_config)
        >>> viability = evaluator.calculate_viability(states, 0.5)
        >>> print(f"Agent viability: {viability:.2f}")
    """
```

### Type Hints

Use comprehensive type hints:

```python
from typing import Dict, List, Optional, Union, Any
from typing_extensions import TypedDict

class TaskMetadata(TypedDict):
    domain: str
    difficulty: Optional[str]
    
def process_tasks(tasks: List[Task], 
                 metadata: TaskMetadata) -> Dict[str, Any]:
    """Process tasks with metadata."""
    pass
```

## 🔌 Plugin Development

### Creating Plugins

1. **Inherit from appropriate base class**
2. **Implement required abstract methods**
3. **Add entry point in `pyproject.toml`**
4. **Include comprehensive tests**
5. **Document usage and configuration**

### Plugin Entry Points

```toml
[project.entry-points."semiosis.agents"]
my_agent = "my_package.agents:MyAgent"

[project.entry-points."semiosis.environments"]
my_env = "my_package.environments:MyEnvironment"
```

## 🎨 Code Style

### Formatting

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

### Pre-commit Hooks

Pre-commit hooks automatically run:
- Black formatting
- isort import sorting
- flake8 linting
- mypy type checking
- Basic security checks

### Code Quality

- Line length: 88 characters (Black default)
- Python 3.9+ compatible
- No unused imports or variables
- Comprehensive type hints
- Clear variable and function names

## 🚦 Pull Request Process

### Before Submitting

1. **Tests pass**: `pytest`
2. **Code formatted**: `black semiosis/ tests/`
3. **Imports sorted**: `isort semiosis/ tests/`
4. **Linting clean**: `flake8 semiosis/ tests/`
5. **Type checking**: `mypy semiosis/`
6. **Documentation updated**: If adding new features

### PR Description Template

```markdown
## Changes
Brief description of what this PR does.

## Related Issue
Closes #XXX

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
- [ ] GitHub issue referenced
```

### Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Documentation review** if applicable
5. **Merge** after approval

## 🌟 Contribution Ideas

### Easy First Issues

- Add new agent adapters (Cohere, Google PaLM, etc.)
- Create example environments for specific domains
- Improve error messages and user experience
- Add visualization options
- Write tutorials and documentation

### Advanced Contributions

- Implement new intervention strategies
- Add support for new context systems
- Optimize performance for large evaluations
- Develop new semantic information metrics
- Create specialized environments

### Research Contributions

- Validate theoretical assumptions empirically
- Compare with other evaluation frameworks
- Explore new applications of semantic information theory
- Develop domain-specific viability functions

## 🏷️ Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

### Release Checklist

1. **Update version** in `pyproject.toml` and `__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Create release branch**: `release/vX.Y.Z`
4. **Run full test suite** including integration tests
5. **Create GitHub release** with tags
6. **Publish to PyPI** via automated pipeline

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and community discussion
- **GitHub Projects**: Development planning and milestone tracking

### Maintainer Response Times

- **Bug reports**: 2-3 business days
- **Feature requests**: 1 week
- **Pull requests**: 3-5 business days
- **Security issues**: Same day

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background, experience level, or personal characteristics.

### Expected Behavior

- **Be respectful** in all interactions
- **Be constructive** in feedback and criticism
- **Be collaborative** and help others learn
- **Be professional** in all communications

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Hostile or aggressive language
- Personal attacks or insults
- Spam or off-topic discussions

### Reporting

Report any violations to [team@answerlayer.com](mailto:team@answerlayer.com). All reports will be reviewed promptly and confidentially.

## 📄 License

By contributing to Semiosis, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Semiosis! Together, we're advancing the field of LLM agent evaluation. 🚀