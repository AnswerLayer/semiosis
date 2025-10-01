---
name: Environment Request
about: Request support for a new evaluation environment or domain
title: '[ENVIRONMENT] Add support for '
labels: ['enhancement', 'environment']
assignees: ''
---

## Environment Description
- **Domain**: [e.g. question-answering, summarization, code review]
- **Task Type**: [e.g. classification, generation, reasoning]
- **Expected Input**: [e.g. text queries, code snippets, documents]
- **Expected Output**: [e.g. classifications, generated text, structured data]

## Benchmarks/Datasets
Are there existing benchmarks for this domain?
- **Benchmark Name**: [e.g. SQuAD, BLEU, CodeBLEU]
- **Dataset Size**: [number of examples]
- **Ground Truth**: Available/Not Available
- **Evaluation Metrics**: [accuracy, F1, BLEU score, custom]
- **Public Availability**: [freely available, requires registration, proprietary]

## Evaluation Methodology
How should agent responses be evaluated in this domain?
- [ ] Exact match with ground truth
- [ ] Execution-based validation (e.g. code execution)
- [ ] LLM-assisted evaluation (e.g. for subjective tasks)
- [ ] Human evaluation required
- [ ] Domain-specific metrics (please describe)

## Context Systems
What external context would agents need access to?
- **Documentation**: [API docs, knowledge bases]
- **Code Repositories**: [codebases, libraries]
- **Databases**: [structured data, schemas]
- **External APIs**: [search, calculation, validation]
- **Domain Tools**: [compilers, analyzers, simulators]

## Semantic Information Theory Applicability
How would SIT concepts apply to this domain?
- **Trust Building**: How should agent trust be measured?
- **Budget Consumption**: What constitutes computational cost?
- **Viability**: What does agent "survival" mean in this context?
- **Context Interventions**: How could context be systematically modified?

## Example Workflow
Describe a typical evaluation scenario:

```
1. Agent receives: [input description]
2. Agent has access to: [context description]
3. Agent should produce: [output description]
4. Success is measured by: [evaluation criteria]
```

## Research Value
Why is this environment important for semantic information research?
- Novel application of SIT principles
- Understudied domain for agent evaluation
- Comparison with existing benchmarks
- Real-world deployment scenario
- Other: [describe]

## Implementation Complexity
What would be involved in implementing this environment?
- [ ] Simple - similar to existing environments
- [ ] Moderate - requires new evaluation logic
- [ ] Complex - requires external integrations
- [ ] Very Complex - requires novel research

## Data Requirements
- **Dataset Size**: [estimated number of examples needed]
- **Ground Truth**: [type and availability]
- **Context Data**: [what external data is needed]
- **Privacy Concerns**: [any sensitive data considerations]

## Example Configuration
How would users configure this environment?

```yaml
environment:
  type: "your-domain"
  dataset: "benchmark-name"
  evaluation_method: "execution"
  context_sources:
    - type: "documentation"
      path: "./docs/"
    - type: "api"
      endpoint: "https://api.example.com"
```

## Related Work
Are there existing tools or frameworks that handle this domain?
- Academic papers
- Open source tools
- Commercial platforms
- Benchmark implementations

## Contribution
Can you help implement this environment?
- [ ] Yes - I have domain expertise
- [ ] Yes - I have access to datasets
- [ ] Yes - I can implement the evaluation logic
- [ ] Yes - I can test and validate
- [ ] No - but I can provide feedback