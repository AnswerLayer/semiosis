"""
DBT Context System implementation.

Provides context from DBT projects by parsing manifest.json files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class DBTContextSystem:
    """
    Context provider for DBT projects.

    Loads models, documentation, and metadata from DBT manifest files
    to provide context for LLM agents.
    """

    def __init__(self, project_path: str):
        """
        Initialize DBT context system.

        Args:
            project_path: Path to DBT project root (should contain target/manifest.json)
        """
        self.project_path = Path(project_path)
        self.manifest: Optional[Dict[str, Any]] = None

    def get_context(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Get DBT context for a query.

        Args:
            query: The query/task that needs context

        Returns:
            Tuple of (context_string, metadata_dict)
        """
        # Load manifest if not already loaded
        if self.manifest is None:
            self._load_manifest()

        # Format context for LLM consumption
        context_parts: List[str] = []
        model_count = 0
        column_count = 0

        # Load models and documentation
        assert self.manifest is not None  # _load_manifest() either sets or raises
        for node_id, node in self.manifest.get("nodes", {}).items():
            if node.get("resource_type") == "model":
                model_count += 1
                context_parts.append(self._format_model(node))
                column_count += len(node.get("columns", {}))

        # Combine all context
        context = "\n\n".join(context_parts) if context_parts else "No models found"

        # Metadata for tracking
        metadata = {
            "source": "dbt",
            "project_path": str(self.project_path),
            "model_count": model_count,
            "column_count": column_count,
            "manifest_version": (
                self.manifest.get("metadata", {}).get("dbt_version")
                if self.manifest
                else None
            ),
            "size": len(context),
        }

        return context, metadata

    def _load_manifest(self):
        """Load manifest.json from DBT project."""
        manifest_path = self.project_path / "target" / "manifest.json"

        if not manifest_path.exists():
            raise FileNotFoundError(
                f"No manifest.json found at {manifest_path}. "
                f"Run 'dbt compile' or 'dbt run' in your DBT project first."
            )

        try:
            with open(manifest_path) as f:
                self.manifest = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in manifest.json: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to load manifest.json: {e}") from e

    def _format_model(self, model: Dict[str, Any]) -> str:
        """Format a DBT model for LLM context."""
        parts = []

        # Model name and basic info
        model_name = model.get("name", "unknown")
        parts.append(f"Model: {model_name}")

        # Description if available
        if model.get("description"):
            parts.append(f"Description: {model['description']}")

        # Materialization info
        materialization = model.get("config", {}).get("materialized", "view")
        parts.append(f"Materialization: {materialization}")

        # Column documentation
        columns = model.get("columns", {})
        if columns:
            parts.append("Columns:")
            for col_name, col_info in columns.items():
                col_desc = col_info.get("description") or "No description"
                parts.append(f"  - {col_name}: {col_desc}")

        # Tags if any
        tags = model.get("tags", [])
        if tags:
            parts.append(f"Tags: {', '.join(tags)}")

        return "\n".join(parts)
