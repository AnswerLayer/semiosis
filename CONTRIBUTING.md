# Contributing to Semiosis

Welcome! This is a minimal, contributor‑friendly guide to get you productive quickly.

## Quick start (60 seconds)

1) Clone and enter the repo
   ```bash
   git clone https://github.com/your-username/semiosis.git
   cd semiosis
   ```

2) Create and activate a virtualenv
   ```bash
   python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3) Install dev deps
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```

4) Verify setup
   ```bash
pytest -q
```

## How to contribute

- **Find or open an issue**: propose ideas, bugs, or improvements.
- **Create a branch**: `your-name/short-description` (e.g., `alex/add-sql-env`).
- **Commit style**: Conventional Commits (e.g., `feat(env): add text-to-sql validation`). Keep messages short.
- **Open a PR**: small and focused is best. Link the issue if there is one.

## Project layout (at a glance)

```
semiosis/
├── agents/          # Agent implementations
├── environments/    # Evaluation environments
├── contexts/        # Context integrations
├── interventions/   # Context interventions
├── sit/             # Semantic Information Theory engine
├── cli/             # Command-line interface
├── evaluation/      # Orchestration
└── plugins/         # Extension points
```

## Quality checks (local)

```bash
# tests
pytest

# format and lint
black semiosis/ tests/
isort semiosis/ tests/
flake8 semiosis/ tests/

# type checking
mypy semiosis/
```

Tips:
- Use markers like `-m "not requires_api"` to skip tests needing API keys.
- Keep PRs small; they review faster and land sooner.

## Lightweight PR checklist

- Changes are scoped and documented in the PR description
- Tests pass locally (`pytest`), or rationale provided if not applicable
- Code formatted and linted (Black, isort, flake8)
- Types checked where applicable (mypy)

## Discussions and help

- Questions or ideas? Open a **GitHub Discussion** or **Issue**.
- For conduct concerns, email: [team@answerlayer.com](mailto:team@answerlayer.com).

## Code of Conduct

Be respectful and constructive. We welcome first‑time contributors.

## License

By contributing, you agree your contributions are under the MIT License.
