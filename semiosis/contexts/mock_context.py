"""
Mock context system implementation for testing and development.

This module provides a mock context system that can be used when specific
context system implementations are not available.
"""

from typing import Any, Dict, List

from semiosis.contexts.base import BaseContextSystem, ContextElement


class MockContextSystem(BaseContextSystem):
    """
    Mock context system implementation for testing and development.

    This context system provides sample context elements for testing the framework
    without requiring specific context provider implementations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the mock context system.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.context_elements = self._generate_sample_context()

    def initialize(self):
        """
        Initialize the context system and its resources.
        """
        print("Mock context system initialized")

    def cleanup(self):
        """
        Clean up context system resources.
        """
        print("Mock context system cleaned up")

    def _generate_sample_context(self) -> List[ContextElement]:
        """
        Generate sample context elements.

        Returns:
            List of sample context elements
        """
        sample_context = [
            {
                "id": "ctx_001",
                "type": "documentation",
                "content": "Database schema: users table with id, name, email columns",
                "relevance": 0.9,
            },
            {
                "id": "ctx_002",
                "type": "code_example",
                "content": "SELECT * FROM users WHERE email LIKE '%@gmail.com';",
                "relevance": 0.8,
            },
            {
                "id": "ctx_003",
                "type": "constraint",
                "content": "Maximum query execution time is 30 seconds",
                "relevance": 0.7,
            },
        ]

        elements = []
        for ctx_data in sample_context:
            element = ContextElement(
                id=ctx_data["id"],
                type=ctx_data["type"],
                content=ctx_data["content"],
                relevance=ctx_data["relevance"],
            )
            elements.append(element)

        return elements

    def extract_context(self) -> List[ContextElement]:
        """
        Extract all available context elements from the system.

        Returns:
            List of ContextElement objects
        """
        return self.context_elements

    def filter_context(
        self, query: str, max_elements: int = None
    ) -> List[ContextElement]:
        """
        Filter context elements relevant to a specific query.

        Args:
            query: The query to match against context
            max_elements: Maximum number of elements to return (None for no limit)

        Returns:
            List of relevant ContextElement objects
        """
        # Simple keyword-based filtering for demo purposes
        query_lower = query.lower()
        relevant_elements = []

        for element in self.context_elements:
            if query_lower in element.content.lower():
                relevant_elements.append(element)

        # If no keyword matches, return all elements with lower relevance
        if not relevant_elements:
            relevant_elements = [
                ContextElement(
                    id=elem.id,
                    type=elem.type,
                    content=elem.content,
                    relevance=elem.relevance * 0.5,  # Reduce relevance for non-matching
                )
                for elem in self.context_elements
            ]

        # Limit to max_elements if specified
        if max_elements:
            relevant_elements = relevant_elements[:max_elements]

        return relevant_elements

    def get_context_size(self) -> int:
        """
        Get the total number of available context elements.

        Returns:
            Total count of context elements
        """
        return len(self.context_elements)
