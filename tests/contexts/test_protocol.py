"""Tests for context provider protocol and interventions."""

from typing import Any, Dict, Tuple

from semiosis.contexts.interventions import (
    apply_intervention,
    compose_interventions,
    remove_percentage,
    shuffle_content,
    truncate_context,
)


class SimpleContext:
    """Test implementation of context provider."""

    def __init__(self, content: str):
        self.content = content

    def get_context(self, query: str) -> Tuple[str, Dict[str, Any]]:
        return self.content, {"source": "test", "query": query}


class TestContextProtocol:
    """Test that the protocol works with duck typing."""

    def test_protocol_satisfied(self):
        """Any object with get_context method satisfies the protocol."""
        provider = SimpleContext("Hello, world!")
        context, metadata = provider.get_context("test query")

        assert context == "Hello, world!"
        assert metadata["source"] == "test"
        assert metadata["query"] == "test query"

    def test_protocol_with_different_class(self):
        """Protocol works with any class structure."""

        class CustomProvider:
            def get_context(self, q: str) -> Tuple[str, Dict[str, Any]]:
                return f"Context for: {q}", {"custom": True}

        provider = CustomProvider()
        context, metadata = provider.get_context("SELECT *")

        assert context == "Context for: SELECT *"
        assert metadata["custom"] is True


class TestInterventions:
    """Test intervention functions."""

    def test_apply_intervention_basic(self):
        """Test basic intervention application."""
        provider = SimpleContext("Line 1\nLine 2\nLine 3")

        # Simple intervention that uppercases content
        def uppercase_intervention(
            content: str, metadata: Dict[str, Any]
        ) -> Tuple[str, Dict[str, Any]]:
            return content.upper(), metadata

        modified = apply_intervention(
            provider, uppercase_intervention, "uppercase", 0.0
        )
        context, metadata = modified.get_context("query")

        assert context == "LINE 1\nLINE 2\nLINE 3"
        assert metadata["interventions"][0]["name"] == "uppercase"
        assert metadata["interventions"][0]["noise_level"] == 0.0

    def test_remove_percentage(self):
        """Test removing percentage of content."""
        lines = [f"Line {i}" for i in range(10)]
        provider = SimpleContext("\n".join(lines))

        # Remove 50% of content
        modified = remove_percentage(provider, 0.5)
        context, metadata = modified.get_context("query")

        result_lines = context.split("\n") if context else []
        assert len(result_lines) == 5
        assert metadata["original_lines"] == 10
        assert metadata["kept_lines"] == 5
        assert metadata["interventions"][0]["noise_level"] == 0.5

        # All kept lines should be from original
        for line in result_lines:
            assert line in lines

    def test_remove_all_content(self):
        """Test removing 100% of content."""
        provider = SimpleContext("Some content")
        modified = remove_percentage(provider, 1.0)
        context, metadata = modified.get_context("query")

        assert context == ""
        assert metadata["kept_lines"] == 0

    def test_shuffle_content(self):
        """Test shuffling content lines."""
        lines = [f"Line {i}" for i in range(5)]
        provider = SimpleContext("\n".join(lines))

        modified = shuffle_content(provider)
        context, metadata = modified.get_context("query")

        result_lines = context.split("\n")
        assert len(result_lines) == 5
        assert set(result_lines) == set(lines)  # Same lines, different order
        assert metadata["shuffled"] is True
        assert metadata["interventions"][0]["noise_level"] == 0.3

    def test_truncate_context(self):
        """Test truncating context to max length."""
        provider = SimpleContext("A" * 1000)

        modified = truncate_context(provider, 100)
        context, metadata = modified.get_context("query")

        assert len(context) == 100
        assert context == "A" * 100
        assert metadata["original_chars"] == 1000
        assert metadata["truncated_chars"] == 100

    def test_compose_interventions(self):
        """Test composing multiple interventions."""
        provider = SimpleContext("Line 1\nLine 2\nLine 3\nLine 4")

        # Compose: remove 50% then shuffle
        composed = compose_interventions(
            lambda p: remove_percentage(p, 0.5), shuffle_content
        )

        modified = composed(provider)
        context, metadata = modified.get_context("query")

        result_lines = context.split("\n") if context else []
        assert len(result_lines) == 2  # 50% of 4
        assert metadata["kept_lines"] == 2
        assert metadata["shuffled"] is True
        assert len(metadata["interventions"]) == 2

    def test_intervention_mutates_provider(self):
        """Test that interventions mutate the provider they're applied to."""
        original_content = "Line 1\nLine 2\nLine 3\nLine 4"

        # Create two separate provider instances
        provider1 = SimpleContext(original_content)
        provider2 = SimpleContext(original_content)

        # Apply intervention to provider1 (mutates it)
        returned = remove_percentage(provider1, 0.5)

        # Verify the intervention mutated provider1
        context1, metadata1 = provider1.get_context("query")
        assert len(context1.split("\n")) == 2  # 50% of 4 lines
        assert metadata1["interventions"][0]["name"] == "remove_50%"
        assert metadata1["interventions"][0]["noise_level"] == 0.5
        assert metadata1["original_lines"] == 4
        assert metadata1["kept_lines"] == 2

        # Verify returned is the same object (mutation, not copy)
        assert returned is provider1

        # Verify provider2 is unaffected (separate instance)
        context2, metadata2 = provider2.get_context("query")
        assert context2 == original_content
        assert "interventions" not in metadata2
