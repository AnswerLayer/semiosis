"""
Command-line interface for Semiosis framework.

This module implements the Click-based CLI framework for the Semiosis evaluation system.
"""

import click
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

from semiosis.cli.factories import create_agent, create_environment, create_context_system
from semiosis.evaluation.runner import EvaluationRunner


@click.group()
@click.version_option()
def cli():
    """Semiosis: Evaluate Semantic Layers for AI Agent Performance."""
    pass


@cli.command()
@click.option('--agent', required=True, help='Agent type to evaluate (e.g., openai, anthropic)')
@click.option('--agent-args', default='', help='Comma-separated key=value pairs for agent configuration')
@click.option('--environment', required=True, help='Environment type for evaluation (e.g., text-to-sql, custom)')
@click.option('--environment-args', default='', help='Comma-separated key=value pairs for environment configuration')
@click.option('--context', default=None, help='Context system type (e.g., dbt, custom)')
@click.option('--context-args', default='', help='Comma-separated key=value pairs for context configuration')
@click.option('--interventions', default='', help='Comma-separated list of interventions to apply')
@click.option('--config-file', default=None, type=click.Path(exists=True), help='YAML configuration file')
@click.option('--output', default='./results.json', help='Output file for results')
def evaluate(agent: str, agent_args: str, environment: str, environment_args: str, 
             context: Optional[str], context_args: str, interventions: str, 
             config_file: Optional[str], output: str):
    """
    Evaluate an agent in a specific environment with optional context and interventions.
    """
    # Parse configuration from file or command line args
    config = _parse_configuration(config_file, agent, agent_args, environment, 
                                  environment_args, context, context_args, interventions)
    
    # Create components using factories
    agent_instance = create_agent(config.get('agent', {}))
    environment_instance = create_environment(config.get('environment', {}))
    context_instance = create_context_system(config.get('context')) if 'context' in config and config.get('context') else None
    
    # Initialize components
    environment_instance.initialize()
    if context_instance:
        context_instance.initialize()
    
    # Create and run evaluation
    runner = EvaluationRunner(agent_instance, environment_instance, context_instance)
    results = runner.run_evaluation()
    
    # Save results
    _save_results(results, output)
    
    click.echo(f"Evaluation completed. Results saved to {output}")


def _parse_configuration(config_file: Optional[str], agent: str, agent_args: str, 
                        environment: str, environment_args: str, context: Optional[str], 
                        context_args: str, interventions: str) -> Dict[str, Any]:
    """
    Parse configuration from file or command line arguments.
    
    Args:
        config_file: Path to YAML config file
        agent: Agent type
        agent_args: Agent arguments
        environment: Environment type
        environment_args: Environment arguments
        context: Context system type
        context_args: Context arguments
        interventions: List of interventions
        
    Returns:
        Configuration dictionary
    """
    config = {}
    
    # Load from config file if provided
    if config_file:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    
    # Override with command line args if provided
    if agent:
        agent_config = config.get('agent', {})
        agent_config['type'] = agent
        agent_config['args'] = _parse_key_value_string(agent_args)
        config['agent'] = agent_config
    
    if environment:
        env_config = config.get('environment', {})
        env_config['type'] = environment
        env_config['args'] = _parse_key_value_string(environment_args)
        config['environment'] = env_config
    
    if context:
        ctx_config = config.get('context', {})
        ctx_config['type'] = context
        ctx_config['args'] = _parse_key_value_string(context_args)
        config['context'] = ctx_config
    
    if interventions:
        config['interventions'] = [i.strip() for i in interventions.split(',') if i.strip()]
    
    return config


def _parse_key_value_string(key_value_string: str) -> Dict[str, Any]:
    """
    Parse a comma-separated key=value string into a dictionary.
    
    Args:
        key_value_string: String in format "key1=value1,key2=value2"
        
    Returns:
        Dictionary with parsed key-value pairs
    """
    if not key_value_string:
        return {}
    
    result = {}
    pairs = key_value_string.split(',')
    
    for pair in pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            # Try to parse as number if possible
            try:
                # Try int first
                result[key] = int(value)
            except ValueError:
                try:
                    # Then float
                    result[key] = float(value)
                except ValueError:
                    # Keep as string
                    result[key] = value
        else:
            # If no equals, treat as boolean flag
            result[pair] = True
    
    return result


def _save_results(results: Any, output_path: str):
    """
    Save evaluation results to a file.
    
    Args:
        results: Evaluation results to save
        output_path: Path to output file
    """
    import json
    
    # Convert results to JSON-serializable format
    serializable_results = _make_serializable(results)
    
    with open(output_path, 'w') as f:
        json.dump(serializable_results, f, indent=2)


def _make_serializable(obj: Any) -> Any:
    """
    Convert an object to a JSON-serializable format.
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON-serializable version of the object
    """
    if hasattr(obj, '__dict__'):
        # Convert dataclass or object to dict
        return {k: _make_serializable(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple)):
        return [_make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    else:
        # Basic types (str, int, float, bool, None) are serializable
        return obj


if __name__ == '__main__':
    cli()