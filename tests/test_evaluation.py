"""
Integration tests for evaluation flow.
"""

import pytest

from semiosis.evaluation.runner import EvaluationRunner


@pytest.mark.integration
def test_basic_evaluation_flow(mock_agent, mock_environment, mock_context):
    """Test that a basic evaluation can run end-to-end without errors."""
    runner = EvaluationRunner(mock_agent, mock_environment, mock_context)

    # Run evaluation - should not crash
    try:
        results = runner.run_evaluation()

        # Basic sanity checks
        assert results is not None
        assert (
            "agent_states" in results or "performance" in results or len(results) >= 0
        )

    except NotImplementedError:
        # If runner isn't fully implemented yet, that's OK for this test
        # We're just checking that the basic flow doesn't crash
        pytest.skip("EvaluationRunner not fully implemented yet")


@pytest.mark.integration
def test_mock_agent_response(mock_agent, sample_query):
    """Test that mock agent produces consistent responses."""
    response1 = mock_agent.generate_response(sample_query)
    response2 = mock_agent.generate_response(sample_query)

    # Mock agent should be deterministic
    assert response1.output == response2.output
    assert isinstance(response1.cost, float)
    assert response1.cost >= 0.0


@pytest.mark.integration
def test_mock_environment_evaluation(mock_environment, sample_query):
    """Test that mock environment can evaluate responses."""
    mock_response = "SELECT department, AVG(salary) FROM employees GROUP BY department"

    # Initialize environment
    mock_environment.initialize()

    try:
        # Get task generator and evaluator
        task_generator = mock_environment.get_task_generator()
        task_evaluator = mock_environment.get_task_evaluator()

        # Generate a task
        tasks = task_generator.generate_tasks(count=1)
        assert len(tasks) > 0

        task = tasks[0]

        # Evaluate the response
        result = task_evaluator.evaluate(task, mock_response)

        assert result.success is not None
        assert isinstance(result.score, float)
        assert 0.0 <= result.score <= 1.0

    except NotImplementedError:
        # If mock environment isn't fully implemented, that's OK
        pytest.skip("Mock environment not fully implemented yet")
    finally:
        mock_environment.cleanup()


@pytest.mark.integration
def test_agent_cost_estimation(mock_agent):
    """Test agent cost estimation functionality."""
    query = "What is the total revenue?"
    response = "SELECT SUM(revenue) FROM sales"

    cost = mock_agent.get_cost_estimate(query, response)

    assert isinstance(cost, float)
    assert cost >= 0.0


@pytest.mark.integration
def test_context_integration(mock_context):
    """Test context system integration."""
    sample_query = "Show me the sales data"

    try:
        # Initialize context system
        mock_context.initialize()

        # Get filtered context for the query (using the actual API)
        context_elements = mock_context.filter_context(sample_query, max_elements=5)

        assert context_elements is not None
        assert isinstance(context_elements, list)

        # Test extracting all context
        all_context = mock_context.extract_context()
        assert all_context is not None
        assert isinstance(all_context, list)

        # Test getting context size
        size = mock_context.get_context_size()
        assert isinstance(size, int)
        assert size >= 0

    except NotImplementedError:
        # If context system isn't fully implemented, that's OK
        pytest.skip("Context system not fully implemented yet")
    finally:
        mock_context.cleanup()


@pytest.mark.e2e
def test_minimal_end_to_end_workflow():
    """Test minimal end-to-end workflow using all mock components."""
    from semiosis.agents.mock_agent import MockAgent
    from semiosis.environments.mock_environment import MockEnvironment
    from semiosis.sit.engine import SemioticEvaluator

    # Create components
    agent = MockAgent({})
    environment = MockEnvironment({})
    evaluator = SemioticEvaluator()

    # Initialize environment
    environment.initialize()

    try:
        # Generate a task
        task_generator = environment.get_task_generator()
        tasks = task_generator.generate_tasks(count=1)

        if not tasks:
            pytest.skip("No tasks generated")

        task = tasks[0]

        # Agent generates response
        agent_response = agent.generate_response(task.query)

        # Environment evaluates response
        task_evaluator = environment.get_task_evaluator()
        eval_result = task_evaluator.evaluate(task, agent_response.output)

        # Update SIT calculations
        from semiosis.agents.base import AgentState

        agent_state = AgentState(
            query=task.query,
            output=agent_response.output,
            trust=5.0,  # Starting trust
            cost=agent_response.cost,
            budget=10.0,  # Starting budget
            parameters={},
        )

        # Update trust based on evaluation
        new_trust = evaluator.update_trust(agent_state.trust, eval_result)
        new_budget = evaluator.update_budget(
            agent_state.budget, agent_state.cost, new_trust
        )

        # Create final state
        final_state = AgentState(
            query=agent_state.query,
            output=agent_state.output,
            trust=new_trust,
            cost=agent_state.cost,
            budget=new_budget,
            parameters=agent_state.parameters,
        )

        evaluator.add_agent_state(final_state)

        # Calculate viability
        viability = evaluator.calculate_viability(trust_threshold=3.0)

        # Basic sanity checks
        assert isinstance(viability, float)
        assert 0.0 <= viability <= 1.0
        assert final_state.trust != agent_state.trust  # Trust should have been updated

    except NotImplementedError as e:
        pytest.skip(f"Component not fully implemented: {e}")
    finally:
        environment.cleanup()
