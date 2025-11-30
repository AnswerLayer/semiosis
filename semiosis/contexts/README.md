# Context System

The context system in Semiosis provides a simple, extensible way to integrate various knowledge sources into agent evaluations.

## Design Philosophy

We use a minimal protocol-based design:
- **No inheritance required** - just implement `get_context(query) -> (str, dict)`
- **Interventions are functions** - easy to compose and test
- **System-specific representations** - no forced abstractions

## Quick Start

### Implementing a Context Provider

Any object with a `get_context` method works:

```python
class MyContext:
    def get_context(self, query: str) -> tuple[str, dict]:
        context = "Relevant information here"
        metadata = {"source": "my_system", "size": len(context)}
        return context, metadata
```

### Applying Interventions

Interventions modify context to measure information density:

```python
from semiosis.contexts import remove_percentage, shuffle_content

# Create provider
provider = MyContext()

# Remove 30% of content
provider = remove_percentage(provider, 0.3)

# Or compose multiple interventions
from semiosis.contexts import compose_interventions
modified = compose_interventions(
    lambda p: remove_percentage(p, 0.5),
    shuffle_content
)(provider)
```

### Metadata Tracking

The metadata dict tracks:
- `source`: Identifier for the context system
- `interventions`: List of applied modifications
- System-specific metrics for analysis

## Contributing

To add a new context provider:

1. Create a class with `get_context(query: str) -> tuple[str, dict]`
2. Format your system's knowledge as a string
3. Include relevant metadata for metrics
4. Add tests demonstrating usage

See `providers/` directory for DBT and file system implementations.
