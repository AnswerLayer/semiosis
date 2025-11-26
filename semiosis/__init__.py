"""
Semiosis: Semantic Information Theory-based Agent Evaluation Framework

A framework for evaluating LLM agents using semantic information theory,
measuring agent viability through trust and budget dynamics.
"""

__version__ = "0.1.0"
__author__ = "AnswerLayer Team"
__email__ = "team@answerlayer.com"
__license__ = "MIT"

from semiosis.agents.base import AgentResponse, AgentState, BaseAgent
from semiosis.contexts.base import BaseContextSystem, ContextElement
from semiosis.environments.base import (
    BaseEnvironment,
    EnvironmentState,
    EvaluationResult,
    Task,
    TaskEvaluator,
    TaskGenerator,
)
from semiosis.interventions.base import BaseIntervention

__all__ = [
    # Core abstractions
    "BaseAgent",
    "AgentResponse",
    "AgentState",
    "BaseEnvironment",
    "TaskGenerator",
    "TaskEvaluator",
    "Task",
    "EvaluationResult",
    "EnvironmentState",
    "BaseContextSystem",
    "ContextElement",
    "BaseIntervention",
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
