"""
Factory functions for creating components from configuration.

This module provides factory functions for creating agents, environments,
and context systems based on configuration parameters.
"""

from typing import Any, Dict, Optional

from semiosis.agents.base import BaseAgent
from semiosis.contexts.base import BaseContextSystem
from semiosis.environments.base import BaseEnvironment


def create_agent(config: Dict[str, Any]) -> BaseAgent:
    """
    Create an agent instance based on configuration.

    Args:
        config: Agent configuration dictionary with 'type' and 'args'

    Returns:
        Instance of the requested agent type
    """
    agent_type = config.get("type", "").lower()
    agent_args = config.get("args", {})

    # Import implementations dynamically to avoid circular dependencies
    if agent_type == "ollama":
        from semiosis.agents.ollama_agent import OllamaAgent

        return OllamaAgent(agent_args)
    elif agent_type == "local":
        # Alias for ollama (user-friendly name)
        from semiosis.agents.ollama_agent import OllamaAgent

        return OllamaAgent(agent_args)
    elif agent_type == "together":
        from semiosis.agents.together_agent import TogetherAgent

        return TogetherAgent(agent_args)
    elif agent_type == "hosted":
        # Alias for together (user-friendly name for hosted open source models)
        from semiosis.agents.together_agent import TogetherAgent

        return TogetherAgent(agent_args)
    else:
        # For now, return a mock agent for other types
        # This will be expanded as more agent types are implemented
        from semiosis.agents.mock_agent import MockAgent

        return MockAgent(agent_args)


def create_environment(config: Dict[str, Any]) -> BaseEnvironment:
    """
    Create an environment instance based on configuration.

    Args:
        config: Environment configuration dictionary with 'type' and 'args'

    Returns:
        Instance of the requested environment type
    """
    env_type = config.get("type", "").lower()
    env_args = config.get("args", {})

    # Import implementations dynamically to avoid circular dependencies
    if env_type == "text-to-sql":
        from semiosis.environments.text_to_sql import TextToSQLEnvironment

        return TextToSQLEnvironment(env_args)
    else:
        # For now, return a mock environment for other types
        from semiosis.environments.mock_environment import MockEnvironment

        return MockEnvironment(env_args)


def create_context_system(
    config: Optional[Dict[str, Any]],
) -> Optional[BaseContextSystem]:
    """
    Create a context system instance based on configuration.

    Args:
        config: Context system configuration dictionary with 'type' and 'args'

    Returns:
        Instance of the requested context system type, or None if config is None
    """
    if config is None:
        return None

    ctx_args = config.get("args", {})

    # Import implementations dynamically to avoid circular dependencies
    # For now, return a mock context system for all types
    # This will be expanded when actual context systems are implemented
    from semiosis.contexts.mock_context import MockContextSystem

    return MockContextSystem(ctx_args)


def _create_component_from_config(component_type: str, config: Dict[str, Any]) -> None:
    """
    Generic helper to create components based on configuration.

    Args:
        component_type: Type of component to create
        config: Configuration dictionary

    Returns:
        Component instance
    """
    # This is a generic helper that can be used for other component types
    # when they're implemented
    pass
