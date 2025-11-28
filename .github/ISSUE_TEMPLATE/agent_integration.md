---
name: Agent Integration
about: Request support for a new LLM agent or provider
title: '[AGENT] Add support for '
labels: ['enhancement', 'agent']
assignees: ''
---

## Agent Details
- **Provider**: [e.g. Cohere, Google PaLM, Mistral AI]
- **Model Names**: [e.g. command-r, gemini-pro, mistral-large]
- **API Documentation**: [link to API docs]

## API Characteristics
- **Authentication**: [API key, OAuth, other]
- **Request Format**: [REST, gRPC, custom]
- **Response Format**: [JSON, streaming, custom]
- **Rate Limits**: [requests per minute/hour]
- **Pricing Model**: [per token, per request, subscription]

## Token Probability Support
Does this API provide token-level probabilities?
- [ ] Yes - returns logprobs for generated tokens
- [ ] Yes - returns logprobs for specific tokens via separate endpoint
- [ ] No - only returns final response
- [ ] Unsure

If yes, please describe the format and any limitations.

## Special Features
Does this agent have any unique capabilities relevant to Semiosis?
- [ ] Function calling / tool use
- [ ] Code execution
- [ ] Multimodal input (images, audio)
- [ ] Custom fine-tuning support
- [ ] Specific domain expertise
- [ ] Other: [describe]

## Use Case
Why do you need this agent integration?
- Research requirements
- Performance comparison
- Cost optimization
- Privacy/security needs
- Domain-specific capabilities
- Other: [describe]

## Implementation Notes
Any specific considerations for implementing this integration?
- Authentication requirements
- Error handling patterns
- Cost estimation methods
- Performance characteristics

## Example Usage
How would you use this agent with Semiosis?

```bash
semiosis evaluate \
    --agent your-provider \
    --agent-args model=model-name,api_key=$API_KEY \
    --environment text-to-sql \
    --context dbt
```

## Documentation/References
- API documentation links
- Example code or SDKs
- Pricing information
- Usage guidelines

## Priority
How important is this integration for your work?
- [ ] High - blocking current research
- [ ] Medium - would be helpful soon
- [ ] Low - nice to have eventually

## Contribution
Are you willing to help implement this integration?
- [ ] Yes - I can implement it
- [ ] Yes - I can help test it
- [ ] Yes - I can provide domain expertise
- [ ] No - but I can test once implemented
