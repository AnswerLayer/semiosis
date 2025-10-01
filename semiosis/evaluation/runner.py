"""
Evaluation runner for coordinating agent-environment interactions.

This module implements the core evaluation orchestration that runs
agent-environment interactions and collects results.
"""

from typing import Any, Dict, List, Optional
from semiosis.agents.base import BaseAgent, AgentState
from semiosis.environments.base import BaseEnvironment, Task, EvaluationResult
from semiosis.contexts.base import BaseContextSystem, ContextElement
from semiosis.interventions.base import BaseIntervention


class EvaluationRunner:
    """
    Coordinates the evaluation loop between agents, environments, and context systems.
    
    This class manages the core evaluation orchestration, tracking progress,
    collecting results, and handling the interaction loop.
    """
    
    def __init__(self, agent: BaseAgent, environment: BaseEnvironment, 
                 context_system: Optional[BaseContextSystem] = None,
                 interventions: Optional[List[BaseIntervention]] = None):
        """
        Initialize the evaluation runner.
        
        Args:
            agent: Agent to evaluate
            environment: Environment to run evaluation in
            context_system: Optional context system to provide context
            interventions: Optional list of interventions to apply
        """
        self.agent = agent
        self.environment = environment
        self.context_system = context_system
        self.interventions = interventions or []
        self.results = []
        self.agent_states = []
        
    def run_evaluation(self) -> Dict[str, Any]:
        """
        Run the complete evaluation loop.
        
        Returns:
            Dictionary containing evaluation results and metadata
        """
        # Initialize environment
        self.environment.initialize()
        
        # Get task generator and evaluator from environment
        task_generator = self.environment.get_task_generator()
        task_evaluator = self.environment.get_task_evaluator()
        
        # Generate tasks
        tasks = task_generator.generate_tasks()
        
        # Run evaluation loop for each task
        for i, task in enumerate(tasks):
            print(f"Processing task {i+1}/{len(tasks)}")
            
            # Get context for this task if context system is available
            context_elements = []
            context_string = ""
            
            if self.context_system:
                context_elements = self.context_system.filter_context(
                    task.query, max_elements=10
                )
                
                # Apply interventions to context if any
                for intervention in self.interventions:
                    context_elements = intervention.apply(context_elements)
                
                context_string = self.context_system.get_context_string(context_elements)
            
            # Generate agent response
            agent_response = self.agent.generate_response(task.query, context_string)
            
            # Evaluate the response
            evaluation_result = task_evaluator.evaluate(task, agent_response.output)
            
            # Track agent state (for SIT calculations)
            agent_state = AgentState(
                query=task.query,
                output=agent_response.output,
                trust=evaluation_result.score,  # Simplified: using score as initial trust
                cost=agent_response.cost,
                budget=100.0,  # Placeholder budget
                parameters=self.agent.config
            )
            
            # Store results
            self.results.append({
                'task_id': task.task_id,
                'query': task.query,
                'response': agent_response.output,
                'ground_truth': task.ground_truth,
                'evaluation': evaluation_result,
                'context_used': len(context_elements),
                'cost': agent_response.cost
            })
            
            self.agent_states.append(agent_state)
            
            # Revert interventions if they were applied
            for intervention in reversed(self.interventions):
                context_elements = intervention.revert(context_elements)
        
        # Cleanup
        self.environment.cleanup()
        
        # Prepare final results
        return self._compile_results()
    
    def _compile_results(self) -> Dict[str, Any]:
        """
        Compile evaluation results into a final report.
        
        Returns:
            Dictionary containing aggregated results and metadata
        """
        total_tasks = len(self.results)
        successful_tasks = sum(1 for r in self.results if r['evaluation'].success)
        total_cost = sum(r['cost'] for r in self.results)
        avg_score = sum(r['evaluation'].score for r in self.results) / total_tasks if total_tasks > 0 else 0
        
        return {
            'summary': {
                'total_tasks': total_tasks,
                'successful_tasks': successful_tasks,
                'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
                'total_cost': total_cost,
                'average_score': avg_score
            },
            'results': self.results,
            'agent_states': self.agent_states,
            'metadata': {
                'agent_type': self.agent.__class__.__name__,
                'environment_type': self.environment.__class__.__name__,
                'context_system_type': self.context_system.__class__.__name__ if self.context_system else None,
                'intervention_count': len(self.interventions)
            }
        }
    
    def get_progress_bar(self, current: int, total: int, bar_length: int = 50) -> str:
        """
        Generate a text-based progress bar.
        
        Args:
            current: Current progress
            total: Total items
            bar_length: Length of the progress bar
            
        Returns:
            String representation of progress bar
        """
        percent = float(current) / total if total > 0 else 0
        filled_length = int(round(bar_length * percent))
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        return f'[{bar}] {current}/{total} ({percent*100:.1f}%)'