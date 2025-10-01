"""
Base classes for environment system.

This module defines the fundamental abstract base classes for the Environment system
that will support all agent evaluation scenarios.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol
from pydantic import BaseModel


@dataclass
class Task:
    """
    Represents a single evaluation task with metadata support.
    
    Attributes:
        query: The input query or task description
        ground_truth: The expected answer or solution
        metadata: Additional information about the task
        task_id: Unique identifier for the task
    """
    query: str
    ground_truth: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None


@dataclass
class EvaluationResult:
    """
    Represents the result of evaluating an agent response.
    
    Attributes:
        success: Whether the evaluation was successful
        score: Numerical score (0.0-1.0) representing performance
        details: Additional evaluation details
        error: Error message if evaluation failed
        metadata: Additional metadata about the result
    """
    success: bool
    score: float
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class EnvironmentState:
    """
    Represents the state of an environment during evaluation.
    
    Attributes:
        resources: Environment-specific resources
        connections: Active connections to external systems
        config: Current environment configuration
    """
    resources: Dict[str, Any]
    connections: Dict[str, Any]
    config: Dict[str, Any]


class TaskGenerator(ABC):
    """
    Abstract base class for generating tasks for evaluation.
    
    This class is responsible for creating Task objects from various data sources,
    including benchmark datasets, custom inputs, or other task sources.
    """
    
    @abstractmethod
    def generate_tasks(self, count: Optional[int] = None, **kwargs) -> List[Task]:
        """
        Generate a list of tasks for evaluation.
        
        Args:
            count: Number of tasks to generate (None for all available)
            **kwargs: Additional configuration options
            
        Returns:
            List of Task objects
        """
        pass
    
    @abstractmethod
    def get_task_count(self) -> int:
        """
        Get the total number of available tasks.
        
        Returns:
            Total number of tasks
        """
        pass


class TaskEvaluator(ABC):
    """
    Abstract base class for evaluating agent responses.
    
    This class is responsible for comparing agent outputs with expected results
    and providing performance scores.
    """
    
    @abstractmethod
    def evaluate(self, task: Task, response: str) -> EvaluationResult:
        """
        Evaluate an agent response against a task.
        
        Args:
            task: The task being evaluated
            response: The agent's response to the task
            
        Returns:
            EvaluationResult containing the evaluation outcome
        """
        pass
    
    @abstractmethod
    def supports_token_level_evaluation(self) -> bool:
        """
        Check if this evaluator supports token-level evaluation.
        
        Returns:
            True if token-level evaluation is supported, False otherwise
        """
        pass


class BaseEnvironment(ABC):
    """
    Abstract base class for all environments in the Semiosis framework.
    
    This class provides the core interface for evaluation environments that will
    support various agent evaluation scenarios.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the environment with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self._state = None
        
    @property
    def state(self) -> Optional[EnvironmentState]:
        """
        Get the current state of the environment.
        
        Returns:
            Current EnvironmentState or None if not initialized
        """
        return self._state
    
    @abstractmethod
    def initialize(self):
        """
        Initialize the environment and its resources.
        """
        pass
    
    @abstractmethod
    def cleanup(self):
        """
        Clean up environment resources.
        """
        pass
    
    @abstractmethod
    def get_task_generator(self) -> TaskGenerator:
        """
        Get the task generator for this environment.
        
        Returns:
            TaskGenerator instance
        """
        pass
    
    @abstractmethod
    def get_task_evaluator(self) -> TaskEvaluator:
        """
        Get the task evaluator for this environment.
        
        Returns:
            TaskEvaluator instance
        """
        pass