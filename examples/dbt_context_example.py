#!/usr/bin/env python3
"""
Example usage of DBT Context System.

This demonstrates how to load context from a DBT project and apply
interventions for SIT experiments.
"""

from semiosis.contexts import DBTContextSystem, remove_percentage


def main():
    """Example usage of DBT context system."""
    # Load DBT context system
    # Replace with path to your DBT project
    dbt_context = DBTContextSystem("./path/to/your/dbt_project")

    try:
        # Get full context
        print("=== Full Context ===")
        context, metadata = dbt_context.get_context("SELECT * FROM users")

        print(
            f"Found {metadata['model_count']} models with {metadata['column_count']} total columns"
        )
        print(f"DBT version: {metadata.get('manifest_version', 'unknown')}")
        print(f"Context size: {metadata['size']} characters")
        print("\nContext preview:")
        print(context[:500] + "..." if len(context) > 500 else context)

        # Apply intervention - remove 30% of context
        print("\n\n=== With 30% Removal Intervention ===")
        modified_context = remove_percentage(dbt_context, 0.3)
        reduced_context, reduced_metadata = modified_context.get_context(
            "SELECT * FROM users"
        )

        print(f"Original lines: {reduced_metadata['original_lines']}")
        print(f"Kept lines: {reduced_metadata['kept_lines']}")
        print(f"Intervention applied: {reduced_metadata['interventions']}")
        print(f"Reduced context size: {len(reduced_context)} characters")
        print("\nReduced context preview:")
        print(
            reduced_context[:300] + "..."
            if len(reduced_context) > 300
            else reduced_context
        )

    except FileNotFoundError:
        print("Error: No manifest.json found.")
        print("Please run 'dbt compile' in your DBT project first.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
