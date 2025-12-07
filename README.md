# Semiosis: Unit Testing for Documentation Quality

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Status](https://img.shields.io/badge/status-alpha-red.svg)

Semiosis is an open-source framework for measuring the semantic quality of static documentation and context systems. Think "unit testing for your knowledge base" - Semiosis reveals how much information is redundant, what's critical, and where your documentation breaks down.

## 🎯 Why Semiosis?

**The Problem**: You've built extensive documentation (DBT projects, API docs, knowledge bases) but don't know if it's actually good. Is there redundancy? What happens if parts go missing? Is it token-efficient?

**The Solution**: Semiosis measures **context system quality** using standardized LLM probes to evaluate:
- **Completeness**: Does your documentation cover all necessary concepts?
- **Redundancy**: How much can you remove while maintaining performance?
- **Semantic Density**: How much information per documentation unit?
- **Robustness**: How gracefully does performance degrade as context is removed?
- **Critical Boundaries**: What's the minimum viable documentation set?

## 🚀 Vision

When complete, Semiosis will provide comprehensive documentation quality analysis:

```bash
# Analyze your DBT project documentation quality
semiosis evaluate \
    --context dbt \
    --context-args project_path=./my_dbt_project \
    --environment text-to-sql \
    --interventions progressive_removal,schema_corruption

# Expected results: context quality report
# 📊 Baseline Performance: 94% (excellent documentation)
# 🎯 Semantic threshold: η_c = 0.35 (robust to 65% removal)
# 💎 Critical components: schema.yml files (high impact)
# 📈 Redundancy: Column descriptions (medium overlap)
# 🏆 Benchmark: 75th percentile vs industry average
```

## 🏗️ Architecture

Semiosis provides a modular framework for context quality measurement:

- **🌍 Environments**: Define evaluation scenarios (text-to-SQL, code generation, custom domains)
- **🤖 Standardized Probes**: Built-in LLM agents as measurement instruments
- **📚 Context Systems**: Integration with documentation sources (DBT, API docs, knowledge bases)
- **⚡ Interventions**: Systematic context modifications (removal, corruption, reordering)
- **📈 Quality Engine**: Mathematical framework for measuring semantic information density

## 🔬 Planned Use Cases

### Documentation Optimization
```bash
# Find minimal documentation set for reliable performance
semiosis evaluate --context dbt --interventions progressive_removal
# Expected: Need only 40% of semantic models for 90% accuracy
```

### Pre-Deployment Validation
```bash
# Test documentation robustness before agent deployment
semiosis evaluate --interventions corruption,missing_schemas,outdated_docs
# Expected: Performance drops to 60% with 30% schema corruption
```

## 📊 Expected Results

- **📈 Quality Curves**: How performance degrades with documentation removal
- **🎯 Semantic Thresholds**: Critical information boundaries (η_c values)
- **💎 Component Analysis**: Which documentation sections are most valuable
- **📊 Redundancy Maps**: What information overlaps and can be consolidated
- **🏆 Benchmarking**: How your context compares to industry standards
- **⚡ Intervention Impact**: Quantified effects of specific documentation changes

## 🛠️ Planned Integrations

### Standardized Measurement Probes
- **Frontier Models**: All your favourites
- **Open Source Models**: SQLCoder, Kimi K2, Mistral, etc.
- **Cloud Platforms**: AWS Bedrock, Google Vertex AI for enterprise deployment

### Evaluation Environments
- **Text-to-SQL**: Spider 2.0, BIRD-SQL datasets for database query generation
- **Code Generation**: Programming task evaluation with execution validation
- **Custom Domains**: YAML-configurable environments for any documentation type

### Documentation Sources
- **DBT Projects**: Schema definitions, model docs, semantic layer analysis
- **API Documentation**: OpenAPI specs, endpoint descriptions, parameter definitions
- **Knowledge Bases**: Markdown files, wikis, technical documentation
- **Custom Sources**: Any structured documentation via plugins

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

- **🌍 Environments**: Create evaluation scenarios for specific domains
- **📚 Context Systems**: Integrate new semantic layer/knowledgebase/documentation technologies

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
@software{semiosis2025,
  title={Semiosis: Evaluate Semantic Layers for AI Agent Performance},
  author={AnswerLayer Team},
  year={2025},
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
