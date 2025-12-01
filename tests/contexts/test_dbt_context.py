"""Tests for DBT context system."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

from semiosis.contexts.providers.dbt_context import DBTContextSystem


class TestDBTContextSystem:
    """Test DBT context system with mock data."""

    @pytest.fixture
    def mock_manifest(self) -> Dict[str, Any]:
        """Mock DBT manifest data."""
        return {
            "metadata": {"dbt_version": "1.7.0", "project_name": "test_project"},
            "nodes": {
                "model.test_project.users": {
                    "name": "users",
                    "resource_type": "model",
                    "description": "User table with basic information",
                    "config": {"materialized": "table"},
                    "columns": {
                        "id": {"name": "id", "description": "Primary key for users"},
                        "email": {"name": "email", "description": "User email address"},
                        "created_at": {
                            "name": "created_at",
                            "description": "When the user was created",
                        },
                    },
                    "tags": ["core", "pii"],
                },
                "model.test_project.orders": {
                    "name": "orders",
                    "resource_type": "model",
                    "description": "Order transactions",
                    "config": {"materialized": "view"},
                    "columns": {
                        "order_id": {
                            "name": "order_id",
                            "description": "Unique identifier for orders",
                        },
                        "user_id": {
                            "name": "user_id",
                            "description": "Foreign key to users table",
                        },
                        "amount": {
                            "name": "amount",
                            "description": "",  # Empty description to test handling
                        },
                    },
                    "tags": [],
                },
                "test.test_project.unique_users_id": {
                    "name": "unique_users_id",
                    "resource_type": "test",  # Should be ignored
                    "description": "Test that user IDs are unique",
                },
            },
        }

    @pytest.fixture
    def temp_dbt_project(self, mock_manifest: Dict[str, Any]):
        """Create temporary DBT project with manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            target_dir = project_path / "target"
            target_dir.mkdir()

            # Write manifest.json
            manifest_path = target_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(mock_manifest, f)

            yield str(project_path)

    def test_basic_context_loading(self, temp_dbt_project: str):
        """Test basic context loading from DBT project."""
        dbt_context = DBTContextSystem(temp_dbt_project)
        context, metadata = dbt_context.get_context("SELECT * FROM users")

        # Check metadata
        assert metadata["source"] == "dbt"
        assert metadata["model_count"] == 2
        assert metadata["column_count"] == 6  # 3 + 3 columns
        assert metadata["manifest_version"] == "1.7.0"
        assert metadata["size"] > 0

        # Check context content
        assert "Model: users" in context
        assert "Model: orders" in context
        assert "User table with basic information" in context
        assert "Primary key for users" in context
        assert "Materialization: table" in context
        assert "Materialization: view" in context
        assert "Tags: core, pii" in context

    def test_empty_descriptions_handled(self, temp_dbt_project: str):
        """Test that empty descriptions are handled gracefully."""
        dbt_context = DBTContextSystem(temp_dbt_project)
        context, metadata = dbt_context.get_context("SELECT amount FROM orders")

        # Empty description should show "No description"
        assert "amount: No description" in context

    def test_missing_manifest_error(self):
        """Test error when manifest.json is missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbt_context = DBTContextSystem(temp_dir)

            with pytest.raises(FileNotFoundError, match="No manifest.json found"):
                dbt_context.get_context("SELECT * FROM users")

    def test_invalid_json_error(self):
        """Test error when manifest.json contains invalid JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            target_dir = project_path / "target"
            target_dir.mkdir()

            # Write invalid JSON
            manifest_path = target_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                f.write("invalid json {")

            dbt_context = DBTContextSystem(temp_dir)

            with pytest.raises(ValueError, match="Invalid JSON"):
                dbt_context.get_context("SELECT * FROM users")

    def test_no_models_in_manifest(self):
        """Test handling when manifest has no models."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)
            target_dir = project_path / "target"
            target_dir.mkdir()

            # Empty manifest
            empty_manifest: Dict[str, Any] = {"metadata": {}, "nodes": {}}
            manifest_path = target_dir / "manifest.json"
            with open(manifest_path, "w") as f:
                json.dump(empty_manifest, f)

            dbt_context = DBTContextSystem(temp_dir)
            context, metadata = dbt_context.get_context("SELECT 1")

            assert context == "No models found"
            assert metadata["model_count"] == 0
            assert metadata["column_count"] == 0

    def test_manifest_caching(self, temp_dbt_project: str):
        """Test that manifest is loaded once and cached."""
        dbt_context = DBTContextSystem(temp_dbt_project)

        # First call loads manifest
        context1, metadata1 = dbt_context.get_context("query1")
        manifest_after_first = dbt_context.manifest

        # Second call should use cached manifest
        context2, metadata2 = dbt_context.get_context("query2")
        manifest_after_second = dbt_context.manifest

        assert manifest_after_first is manifest_after_second
        assert context1 == context2  # Same context regardless of query for now
