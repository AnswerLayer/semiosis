# Semiosis: Evaluate Semantic Layers for AI Agent Performance

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-alpha-red.svg)

Semiosis is an open-source framework for evaluating how well semantic layers support AI agent performance. Instead of just measuring accuracy, Semiosis reveals which contextual information agents actually need to maintain reliable operation over time.

## 🎯 Why Semiosis?

**The Problem**: Traditional AI evaluation focuses on single-shot accuracy. But in production, agents need sustained performance with varying context quality and computational constraints.

**The Solution**: Semiosis measures **agent viability** - how well agents maintain performance while managing real-world constraints like:
- **Incomplete Context**: Missing or degraded semantic information
- **Resource Limits**: Token budgets and computational costs  
- **Trust Dynamics**: Performance feedback affecting future decisions
- **Context Interventions**: Systematic modifications to measure impact

## 🚀 Vision

When complete, Semiosis will enable evaluation of semantic layers for AI agent performance:

```bash
# Future CLI (in development)
semiosis evaluate \
    --agent openai \
    --agent-args model=gpt-4,api_key=$OPENAI_API_KEY \
    --environment text-to-sql \
    --environment-args task_source=spider2 \
    --context dbt \
    --context-args project_path=./my_dbt_project \
    --interventions dbt.add_semantic_model,dbt.remove_documentation

# Expected results: semantic thresholds and viability curves
# 📊 Agent maintained 85% performance with 60% context removal
# 🎯 Semantic threshold: η_c = 0.3 (critical information boundary)
```

## 🛠️ Current Status

**Alpha Development**: We're building the core framework. See [GitHub Issues](https://github.com/AnswerLayer/semiosis/issues) for current progress.

**Phase 1 (In Progress)**: Core abstractions and basic evaluation loop  
**Phase 2 (Planned)**: Semantic Information Theory engine  
**Phase 3 (Planned)**: Extended integrations and custom environments  
**Phase 4 (Planned)**: Community features and distribution

## 🏗️ Planned Architecture

Semiosis will provide a modular framework inspired by the LM Evaluation Harness:

- **🌍 Environments**: Define evaluation scenarios (text-to-SQL, code generation, custom domains)
- **🤖 Agents**: Support multiple LLM providers (OpenAI, Anthropic, local models, remote APIs)
- **📚 Context Systems**: Integration with semantic layers (DBT, GraphRAG, custom MCP servers)
- **⚡ Interventions**: Systematic context modifications to measure robustness
- **📈 Viability Engine**: Mathematical framework for measuring agent sustainability

## 🔬 Planned Use Cases

### Context Optimization
```bash
# Find minimal context for reliable performance (future feature)
semiosis evaluate --context dbt --interventions progressive_removal
# Expected: Agent needs only 40% of semantic models for 90% accuracy
```

### Multi-Agent Comparison
```bash
# Compare how different agents handle context degradation (future feature)
semiosis evaluate --agent openai,anthropic,local --environment custom
# Expected: Claude maintains performance longer under context stress
```

### Production Readiness
```bash
# Test agent robustness before deployment (future feature)
semiosis evaluate --interventions noise,removal,reordering
# Expected: Agent fails below 50% context quality - needs fallback strategy
```

## 📊 Expected Results

- **📈 Viability Curves**: How performance degrades with context removal
- **🎯 Semantic Thresholds**: Critical information boundaries for reliable operation  
- **💰 Cost Analysis**: Resource consumption vs. performance tradeoffs
- **🔄 Trust Dynamics**: How agents build and lose confidence over time
- **📊 Intervention Impact**: Quantified effects of context modifications

## 🛠️ Planned Integrations

### Agents
- **OpenAI**: GPT-3.5, GPT-4, GPT-4o with token probability extraction
- **Anthropic**: Claude 3.x models with message API integration
- **Local Models**: Hugging Face Transformers, vLLM, custom implementations
- **Remote APIs**: HTTP/gRPC agents with custom authentication

### Environments  
- **Text-to-SQL**: Spider 2.0 (632 real-world queries), BIRD-SQL (12,751 examples)
- **Code Generation**: Test suite integration with execution validation
- **Custom Domains**: YAML-configurable environments for any evaluation scenario

### Context Systems
- **DBT**: Data Build Tool semantic layer extraction and manipulation
- **GraphRAG**: Microsoft's graph-based retrieval augmentation
- **Custom MCP**: Model Context Protocol server integrations

## 🧮 Mathematical Foundation

Semiosis will implement a rigorous mathematical framework based on semantic information theory:

```
Agent state:              𝐚 = (q, y, ℓ, c, b, θ)
Environment state:        𝐞 = (D, Q, T)  
Context system:           𝒮_η = [s₁, …, sₙ]
Intervention:             𝒮_η' = 𝒮_η + s_{n+1}
Agent output:             p_θ(y | q, D, 𝒮_η)
Token probability:        p_θ(tᵢ | t_{<i}, q, D, 𝒮_η)
Log-likelihood:           LL_η(t) = Σᵢ log p_θ(tᵢ | t_{<i}, q, D, 𝒮_η)
Cross-entropy:            H_η = 𝔼[−LL_η(t(q))]
Trust update:             ℓ' = ℓ + f(LL(t))
Budget update:            b' = b − c + g(ℓ')
Viability:                V(η) = Pr(ℓ > ℓ_min ∧ b > 0)
Semantic threshold:       η_c = inf{η | V(η) ≤ ½V(1)}
```

Where agents maintain **trust** (ℓ) through performance and **budget** (b) through resource management, with **viability** measuring sustainable operation probability.

## 🤝 Contributing

We welcome contributions! Key areas for community involvement:

- **🔌 Agent Adapters**: Add support for new LLM providers
- **🌍 Environments**: Create evaluation scenarios for specific domains  
- **📚 Context Systems**: Integrate new semantic layer technologies
- **⚡ Interventions**: Develop novel context modification strategies

See our [Contributing Guide](CONTRIBUTING.md) for detailed instructions.

### Development Setup

```bash
git clone https://github.com/AnswerLayer/semiosis.git
cd semiosis
pip install -e ".[dev]"
# Note: Core framework still in development - tests coming soon
```

## 📚 Citation

If you use Semiosis in your research, please cite:

```bibtex
@software{semiosis2024,
  title={Semiosis: Evaluate Semantic Layers for AI Agent Performance},
  author={AnswerLayer Team},
  year={2024},
  url={https://github.com/AnswerLayer/semiosis}
}
```

## 📖 References

This framework builds on foundational work in semantic information theory:

**[1]** Kolchinsky, A. and Wolpert, D.H. Semantic information, autonomous agency, and nonequilibrium statistical physics. *New Journal of Physics*, 20(9):093024, 2018. [arXiv:1806.08053](https://arxiv.org/pdf/1806.08053)

**[2]** Sowinski, D.R., Balasubramanian, V., and Kolchinsky, A. Semantic information in a model of resource gathering agents. *Physical Review E*, 107(4):044404, 2023. [arXiv:2304.03286](https://arxiv.org/pdf/2304.03286)

**[3]** Balasubramanian, V. and Kolchinsky, A. Exo-Daisy World: Revisiting Gaia Theory through an Informational Architecture Perspective. *Planetary Science Journal*, 4(12):236, 2023. [PSJ](https://iopscience.iop.org/article/10.3847/PSJ/ade310)

**[4]** Sowinski, D.R., Frank, A., and Ghoshal, G. Information-theoretic description of a feedback-control Kuramoto model. *Physical Review Research* 6, 043188, 2024. [arXiv:2505.20315](https://arxiv.org/pdf/2505.20315)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **[GitHub Issues](https://github.com/AnswerLayer/semiosis/issues)** - Bug reports and feature requests
- **[GitHub Discussions](https://github.com/AnswerLayer/semiosis/discussions)** - Community discussion  
- **[AnswerLayer](https://answerlayer.com)** - Parent organization

---

**Status**: Alpha - Active development. APIs may change.

**Roadmap**: See [GitHub Issues](https://github.com/AnswerLayer/semiosis/issues/1) for current development plan.