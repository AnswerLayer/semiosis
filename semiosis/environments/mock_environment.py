"""
Mock environment implementation for testing and development.

This module provides a mock environment that can be used when specific
environment implementations are not available.
"""

from typing import Any, Dict, List, Optional

from semiosis.environments.base import (
    BaseEnvironment,
    EvaluationResult,
    Task,
    TaskEvaluator,
    TaskGenerator,
)


class MockTaskGenerator(TaskGenerator):
    """
    Mock task generator for generating sample tasks.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the mock task generator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.tasks = self._generate_sample_tasks()

    def _generate_sample_tasks(self) -> List[Task]:
        """
        Generate sample tasks for the mock environment.

        Returns:
            List of sample tasks
        """
        sample_tasks = [
            {
                "query": "What is the capital of France?",
                "ground_truth": "Paris",
                "task_id": "mock_001",
            },
            {
                "query": "Explain the theory of relativity in simple terms.",
                "ground_truth": "Einstein's theory describing space-time fabric.",
                "task_id": "mock_002",
            },
            {
                "query": "How do you reverse a linked list?",
                "ground_truth": "Iterate and reverse pointers.",
                "task_id": "mock_003",
            },
        ]

        tasks = []
        for task_data in sample_tasks:
            task = Task(
                query=task_data["query"],
                ground_truth=task_data["ground_truth"],
                task_id=task_data["task_id"],
                metadata={"domain": "general_knowledge"},
            )
            tasks.append(task)

        return tasks

    def generate_tasks(self, count: Optional[int] = None, **kwargs) -> List[Task]:
        """
        Generate a list of tasks for evaluation.

        Args:
            count: Number of tasks to generate (None for all available)
            **kwargs: Additional configuration options

        Returns:
            List of Task objects
        """
        if count is None:
            return self.tasks
        else:
            return self.tasks[: min(count, len(self.tasks))]

    def get_task_count(self) -> int:
        """
        Get the total number of available tasks.

        Returns:
            Total number of tasks
        """
        return len(self.tasks)


class MockTaskEvaluator(TaskEvaluator):
    """
    Mock task evaluator for evaluating responses in a test environment.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the mock task evaluator.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.similarity_threshold = config.get("similarity_threshold", 0.7)

    def evaluate(self, task: Task, response: str) -> EvaluationResult:
        """
        Evaluate an agent response against a task.

        Args:
            task: The task being evaluated
            response: The agent's response to the task

        Returns:
            EvaluationResult containing the evaluation outcome
        """
        if not task.ground_truth:
            return EvaluationResult(
                success=True,
                score=1.0,
                details={"reason": "No ground truth provided, assuming success"},
            )

        # Simple similarity check (in practice, this would be more sophisticated)
        similarity = self._calculate_similarity(
            task.ground_truth.lower(), response.lower()
        )
        success = similarity >= self.similarity_threshold
        score = min(1.0, similarity)

        return EvaluationResult(
            success=success,
            score=score,
            details={
                "similarity": similarity,
                "threshold": self.similarity_threshold,
                "ground_truth": task.ground_truth,
                "response": response,
            },
        )

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings.

        Args:
            str1: First string
            str2: Second string

        Returns:
            Similarity score between 0 and 1
        """
        # Simple word overlap similarity
        words1 = set(str1.split())
        words2 = set(str2.split())

        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    def supports_token_level_evaluation(self) -> bool:
        """
        Check if this evaluator supports token-level evaluation.

        Returns:
            True if token-level evaluation is supported, False otherwise
        """
        return False


class MockEnvironment(BaseEnvironment):
    """
    Mock environment implementation for testing and development.

    This environment provides basic functionality for testing the framework
    without requiring specific domain implementations.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the mock environment.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.task_generator = MockTaskGenerator(config or {})
        self.task_evaluator = MockTaskEvaluator(config or {})

    def initialize(self):
        """
        Initialize the environment and its resources.
        """
        print("Mock environment initialized")

    def cleanup(self):
        """
        Clean up environment resources.
        """
        print("Mock environment cleaned up")

    def get_task_generator(self) -> MockTaskGenerator:
        """
        Get the task generator for this environment.

        Returns:
            TaskGenerator instance
        """
        return self.task_generator

    def get_task_evaluator(self) -> MockTaskEvaluator:
        """
        Get the task evaluator for this environment.

        Returns:
            TaskEvaluator instance
        """
        return self.task_evaluator
