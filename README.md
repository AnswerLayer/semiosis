# Semiosis: Semantic Information Theory-based Agent Evaluation Framework

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-alpha-red.svg)

Semiosis is an open-source command-line tool for evaluating LLM agents using Semantic Information Theory (SIT). Inspired by the Sowinsky et al. 2023 paper, it measures how well agents maintain viability through their context systems by analyzing semantic information flow and intervention effects.

## 🎯 Core Concept

Traditional agent evaluation focuses on accuracy metrics. Semiosis evaluates **agent viability** - the ability to maintain performance while managing computational resources through trust and budget dynamics.

### Key Metrics

- **Viability Function**: `V(η) = Pr(ℓ > ℓ_min ∧ b > 0)` - probability of maintaining sufficient trust and budget
- **Semantic Threshold**: `η_c` - critical information boundary where agent performance degrades
- **Trust Dynamics**: Performance-based confidence accumulation over time
- **Budget Management**: Resource consumption and replenishment based on trust

## 🚀 Quick Start

```bash
# Install from PyPI (coming soon)
pip install semiosis

# Basic evaluation with OpenAI agent and DBT context
semiosis evaluate \
    --agent openai \
    --agent-args model=gpt-4,api_key=$OPENAI_API_KEY \
    --environment text-to-sql \
    --environment-args task_source=spider2,databases=./spider_dbs \
    --context dbt \
    --context-args project_path=./my_dbt_project \
    --interventions dbt.add_semantic_model,dbt.remove_documentation
```

## 🏗️ Architecture

Semiosis uses a modular architecture inspired by the LM Evaluation Harness:

- **Environments**: Define evaluation scenarios (text-to-SQL, code generation, custom)
- **Agents**: Support multiple LLM providers (OpenAI, Anthropic, local models)
- **Context Systems**: Integration with external knowledge (DBT, GraphRAG, MCP)
- **Interventions**: Systematic context modifications for semantic analysis
- **SIT Engine**: Semantic Information Theory calculations and viability analysis

## 📊 Example Results

![Viability Curve](docs/images/viability_curve.png)

The semantic threshold (η_c) identifies the critical point where context information becomes essential for agent viability.

## 🔬 Research Applications

- **Context Optimization**: Find minimal viable information for agent deployment
- **Robustness Analysis**: Measure agent resilience to context degradation
- **Resource Planning**: Optimize computational budgets for sustained performance
- **Comparative Evaluation**: Benchmark agents beyond traditional accuracy metrics

## 🛠️ Supported Integrations

### Agents
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- Anthropic (Claude 3.x)
- Local models (via Hugging Face, vLLM)
- Remote HTTP/gRPC agents

### Environments  
- Text-to-SQL (Spider 2.0, BIRD-SQL)
- Code Generation
- Custom YAML-defined environments

### Context Systems
- DBT (Data Build Tool)
- GraphRAG (coming soon)
- Custom MCP integrations

## 📖 Documentation

- [Getting Started](docs/getting-started/installation.md)
- [Concepts](docs/concepts/semantic-information-theory.md)
- [Tutorials](docs/tutorials/text-to-sql-evaluation.md)
- [API Reference](docs/api-reference/core-classes.md)

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/answerlayer/semiosis.git
cd semiosis
pip install -e ".[dev]"
pytest tests/
```

## 📚 Citation

If you use Semiosis in your research, please cite:

```bibtex
@software{semiosis2024,
  title={Semiosis: Semantic Information Theory-based Agent Evaluation Framework},
  author={AnswerLayer Team},
  year={2024},
  url={https://github.com/answerlayer/semiosis}
}
```

Original theoretical foundation:
```bibtex
@article{sowinski2023semantic,
  title={Semantic Information in a model of Resource Gathering Agents},
  author={Sowinski, Damian R. and others},
  journal={PRX Life},
  year={2023}
}
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Issues](https://github.com/answerlayer/semiosis/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/answerlayer/semiosis/discussions) - Community discussion
- [AnswerLayer](https://answerlayer.com) - Parent organization
- [Research Paper](https://arxiv.org/abs/2304.03286) - Theoretical foundation

---

**Status**: Alpha - Active development. APIs may change.

**Roadmap**: See [GitHub Projects](https://github.com/answerlayer/semiosis/projects) for current development plan.