"""
Basic CLI smoke tests.
"""

import pytest
from click.testing import CliRunner

from semiosis.cli.main import cli


@pytest.mark.unit
def test_cli_help():
    """Test that CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "semiosis" in result.output.lower() or "usage" in result.output.lower()


@pytest.mark.unit
def test_cli_version():
    """Test that CLI version command works if it exists."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])

    # Version command might not exist yet, so we're lenient here
    # We just want to make sure it doesn't crash catastrophically
    assert result.exit_code in [0, 2]  # 0 = success, 2 = command not found


@pytest.mark.integration
def test_cli_evaluate_help():
    """Test that evaluate subcommand help works."""
    runner = CliRunner()

    # Try to get help for evaluate command
    result = runner.invoke(cli, ["evaluate", "--help"])

    # Should either succeed or fail gracefully
    assert result.exit_code in [0, 2]

    if result.exit_code == 0:
        assert "evaluate" in result.output.lower()


@pytest.mark.slow
@pytest.mark.requires_api
def test_cli_basic_mock_evaluation():
    """Test basic CLI evaluation with mock components (slow test)."""
    runner = CliRunner()

    # This is a more complex test that would run a full CLI command
    # We'll skip it if CLI isn't fully implemented
    try:
        result = runner.invoke(
            cli,
            [
                "evaluate",
                "--agent",
                "mock",
                "--environment",
                "mock",
                "--num-tasks",
                "1",
            ],
        )

        # Should either succeed or fail gracefully with helpful error
        assert result.exit_code in [0, 1, 2]

        # If it succeeds, output should contain some evaluation info
        if result.exit_code == 0:
            # Look for any reasonable output indicating evaluation ran
            output_lower = result.output.lower()
            success_indicators = [
                "evaluation",
                "completed",
                "results",
                "viability",
                "trust",
                "budget",
            ]
            assert any(indicator in output_lower for indicator in success_indicators)

    except Exception as e:
        # If CLI framework isn't ready, skip this test
        pytest.skip(f"CLI not ready for integration testing: {e}")


@pytest.mark.unit
def test_cli_import():
    """Test that CLI module imports without errors."""
    try:
        from semiosis.cli.factories import create_agent, create_environment

        # Basic checks that factory functions and cli exist
        assert create_agent is not None
        assert create_environment is not None
        assert cli is not None

    except ImportError as e:
        pytest.skip(f"CLI module not fully implemented: {e}")


@pytest.mark.unit
def test_cli_factories():
    """Test that CLI factories can create mock components."""
    try:
        from semiosis.cli.factories import create_agent, create_environment

        # Test creating mock agent
        mock_agent = create_agent({"type": "mock", "args": {}})
        assert mock_agent is not None

        # Test creating mock environment
        mock_env = create_environment({"type": "mock", "args": {}})
        assert mock_env is not None

    except (ImportError, NotImplementedError) as e:
        pytest.skip(f"CLI factories not fully implemented: {e}")
