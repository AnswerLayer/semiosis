# Pull Request

## Changes
Brief description of what this PR does.

## Related Issue
- Closes #XXX
- Related to #XXX

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test coverage improvement

## Component Areas
Which parts of Semiosis does this change affect?
- [ ] Agents (OpenAI, Anthropic, local models)
- [ ] Environments (text-to-SQL, code generation, custom)
- [ ] Context Systems (DBT, GraphRAG, MCP)
- [ ] Interventions (context modifications)
- [ ] SIT Engine (semantic information calculations)
- [ ] CLI (command-line interface)
- [ ] Visualization (results and reporting)
- [ ] Plugins (extension system)
- [ ] Documentation
- [ ] Tests
- [ ] CI/CD

## Testing
- [ ] Added unit tests for new functionality
- [ ] Added integration tests where appropriate
- [ ] Updated existing tests that were affected
- [ ] Manual testing completed
- [ ] All tests pass locally

## Code Quality
- [ ] Code follows the style guidelines (black, isort, flake8)
- [ ] Type hints added for new functions/methods
- [ ] Docstrings added for public interfaces
- [ ] Self-review of the code completed
- [ ] Comments added for complex logic

## Documentation
- [ ] Updated relevant documentation
- [ ] Added docstrings for new functions/classes
- [ ] Updated CLI help text if applicable
- [ ] Added example usage if introducing new features
- [ ] Updated CHANGELOG.md

## Breaking Changes
If this introduces breaking changes, please describe:
- What breaks and why
- Migration path for users
- Version impact (major/minor/patch)

## Performance Impact
Does this change affect performance?
- [ ] No performance impact
- [ ] Performance improvement
- [ ] Performance regression (justified because...)
- [ ] Unknown - performance testing needed

## API Changes
If this changes public APIs, please describe:
- New methods/functions added
- Existing methods/functions modified
- Parameters added/removed/changed
- Return value changes

## Configuration Changes
If this affects configuration:
- [ ] New configuration options added
- [ ] Existing configuration options changed
- [ ] Default values changed
- [ ] Configuration validation updated

## Deployment Notes
Any special considerations for deployment:
- New dependencies added
- Environment variable changes
- Database schema changes
- File system requirements

## Screenshots/Examples
If applicable, add screenshots or example output:

```bash
# Example command
semiosis evaluate --agent openai --environment text-to-sql
```

```
Example output or behavior change
```

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated and passing
- [ ] GitHub issue referenced
- [ ] Breaking changes documented
- [ ] Performance impact considered

## Additional Notes
Any other information that reviewers should know about this change.