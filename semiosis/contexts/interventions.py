"""
Context intervention functions.

Interventions modify context providers to systematically alter the information
available to agents, enabling semantic information theory experiments.
"""

import random
from typing import Any, Callable, Dict, Tuple


def apply_intervention(
    provider: Any,
    intervention_fn: Callable[[str, Dict[str, Any]], Tuple[str, Dict[str, Any]]],
    name: str,
    noise_level: float,
) -> Any:
    """
    Apply an intervention function to a context provider.

    Args:
        provider: Any object with a get_context method
        intervention_fn: Function that modifies (context, metadata) tuple
        name: Name of the intervention for tracking
        noise_level: Estimated information reduction (0.0 to 1.0)

    Returns:
        The provider with modified get_context behavior
    """
    original_get_context = provider.get_context

    def modified_get_context(query: str) -> Tuple[str, Dict[str, Any]]:
        context, metadata = original_get_context(query)

        # Apply the intervention
        modified_context, modified_metadata = intervention_fn(context, metadata)

        # Track intervention in metadata
        modified_metadata["interventions"] = metadata.get("interventions", []) + [
            {"name": name, "noise_level": noise_level}
        ]

        return modified_context, modified_metadata

    provider.get_context = modified_get_context
    return provider


def remove_percentage(provider: Any, percentage: float) -> Any:
    """
    Remove a percentage of content from the context.

    Args:
        provider: Context provider to modify
        percentage: Percentage to remove (0.0 to 1.0)

    Returns:
        Modified provider
    """

    def intervention_fn(
        context: str, metadata: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        lines = context.split("\n")
        keep_count = int(len(lines) * (1 - percentage))
        kept_lines = random.sample(lines, keep_count) if keep_count > 0 else []

        metadata = metadata.copy()
        metadata["original_lines"] = len(lines)
        metadata["kept_lines"] = len(kept_lines)

        return "\n".join(kept_lines), metadata

    return apply_intervention(
        provider, intervention_fn, f"remove_{int(percentage * 100)}%", percentage
    )


def shuffle_content(provider: Any) -> Any:
    """
    Shuffle the order of context content lines.

    Args:
        provider: Context provider to modify

    Returns:
        Modified provider with shuffled content
    """

    def intervention_fn(
        context: str, metadata: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        lines = context.split("\n")
        shuffled = lines.copy()
        random.shuffle(shuffled)

        metadata = metadata.copy()
        metadata["shuffled"] = True

        return "\n".join(shuffled), metadata

    return apply_intervention(
        provider,
        intervention_fn,
        "shuffle_content",
        0.3,  # Moderate noise - content intact but order lost
    )


def truncate_context(provider: Any, max_chars: int) -> Any:
    """
    Truncate context to a maximum character length.

    Args:
        provider: Context provider to modify
        max_chars: Maximum characters to keep

    Returns:
        Modified provider with truncated content
    """

    def intervention_fn(
        context: str, metadata: Dict[str, Any]
    ) -> Tuple[str, Dict[str, Any]]:
        original_length = len(context)
        truncated = context[:max_chars]

        metadata = metadata.copy()
        metadata["original_chars"] = original_length
        metadata["truncated_chars"] = len(truncated)

        return truncated, metadata

    noise = 1.0 - (max_chars / 10000)  # Assume 10k chars is "full" context
    return apply_intervention(
        provider, intervention_fn, f"truncate_{max_chars}", max(0, min(1, noise))
    )


def compose_interventions(*interventions: Callable) -> Callable:
    """
    Compose multiple intervention functions into one.

    Args:
        *interventions: Functions that take and return a provider

    Returns:
        A function that applies all interventions in order
    """

    def composed(provider: Any) -> Any:
        result = provider
        for intervention in interventions:
            result = intervention(result)
        return result

    return composed
