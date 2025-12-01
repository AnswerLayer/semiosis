"""
Context Provider Protocol for Semiosis.

This module defines the minimal protocol that all context providers must follow.
The design prioritizes simplicity and extensibility over complex abstractions.
"""

from typing import Any, Dict, Protocol, Tuple


class ContextProvider(Protocol):
    """
    Protocol for any object that can provide context for agent queries.

    Context providers load and format information from their source systems
    (DBT projects, file systems, APIs, etc.) for LLM consumption.

    Example:
        >>> class MyContext:
        ...     def get_context(self, query: str) -> Tuple[str, Dict[str, Any]]:
        ...         return "Relevant context here", {"source": "my_system"}
        >>>
        >>> provider = MyContext()
        >>> context, metadata = provider.get_context("SELECT * FROM users")
    """

    def get_context(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Get context relevant to a query.

        Args:
            query: The query/task that needs context (e.g., SQL query, question)

        Returns:
            A tuple of:
            - context_string: Formatted context for LLM consumption
            - metadata: Dictionary with details about the context (source, size, etc.)

        The metadata dict should include at minimum:
        - source: Identifier for the context system (e.g., "dbt", "filesystem")
        - Any intervention tracking if context was modified

        Additional metadata is system-specific and used for metrics/debugging.
        """
        ...
