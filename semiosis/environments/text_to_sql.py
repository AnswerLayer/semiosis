"""
Text-to-SQL environment implementation.

This module implements the TextToSQLEnvironment as the primary reference 
implementation, including Spider 2.0 integration and SQL execution validation.
"""

import sqlite3
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import time

from semiosis.environments.base import (
    BaseEnvironment, TaskGenerator, TaskEvaluator, Task, EvaluationResult
)


@dataclass
class SQLTask(Task):
    """
    Extended Task class for SQL-specific tasks.
    
    Attributes:
        query: Natural language question
        ground_truth: Correct SQL query
        database_path: Path to the database for this task
        expected_result: Expected result of executing the SQL query
    """
    database_path: Optional[str] = None
    expected_result: Optional[List[Dict[str, Any]]] = None


class Spider2TaskGenerator(TaskGenerator):
    """
    Task generator for Spider 2.0 dataset.
    
    This class loads and parses the Spider 2.0 dataset, providing tasks
    for text-to-SQL evaluation.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Spider 2.0 task generator.
        
        Args:
            config: Configuration dictionary with dataset paths and options
        """
        self.config = config
        self.dataset_path = config.get('dataset_path', './spider2_dataset')
        self.database_path = config.get('database_path', './spider2_databases')
        self.subset_size = config.get('subset_size', None)  # None for full dataset
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[SQLTask]:
        """
        Load tasks from the Spider 2.0 dataset.
        
        Returns:
            List of SQLTask objects
        """
        # This is a placeholder implementation
        # In a real implementation, this would load from actual Spider 2.0 data
        tasks = []
        
        # For demonstration, creating sample tasks
        # In real implementation, this would parse the actual Spider 2.0 JSON files
        sample_tasks = [
            {
                "query": "Find the name of all students who are enrolled in the Computer Science department.",
                "ground_truth": "SELECT name FROM students WHERE department = 'Computer Science';",
                "database_path": "./sample_dbs/university.db",
                "expected_result": [{"name": "John Doe"}, {"name": "Jane Smith"}],
                "task_id": "spider2_001"
            },
            {
                "query": "What is the average salary of employees in the Engineering department?",
                "ground_truth": "SELECT AVG(salary) FROM employees WHERE department = 'Engineering';",
                "database_path": "./sample_dbs/company.db",
                "expected_result": [{"AVG(salary)": 75000}],
                "task_id": "spider2_002"
            }
        ]
        
        for i, task_data in enumerate(sample_tasks):
            if self.subset_size and i >= self.subset_size:
                break
                
            task = SQLTask(
                query=task_data["query"],
                ground_truth=task_data["ground_truth"],
                database_path=task_data["database_path"],
                expected_result=task_data["expected_result"],
                task_id=task_data["task_id"]
            )
            tasks.append(task)
        
        return tasks
    
    def generate_tasks(self, count: Optional[int] = None, **kwargs) -> List[Task]:
        """
        Generate a list of SQL tasks.
        
        Args:
            count: Number of tasks to generate (None for all available)
            **kwargs: Additional configuration options
            
        Returns:
            List of Task objects
        """
        if count is None:
            return self.tasks
        else:
            return self.tasks[:min(count, len(self.tasks))]
    
    def get_task_count(self) -> int:
        """
        Get the total number of available tasks.
        
        Returns:
            Total number of tasks
        """
        return len(self.tasks)


class SQLTaskEvaluator(TaskEvaluator):
    """
    Task evaluator for SQL tasks.
    
    This class executes SQL queries and compares results to validate correctness.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the SQL task evaluator.
        
        Args:
            config: Configuration dictionary with evaluation options
        """
        self.config = config
        self.timeout = config.get('timeout', 30)  # 30 seconds default timeout
    
    def evaluate(self, task: Task, response: str) -> EvaluationResult:
        """
        Evaluate a SQL response by executing both the generated and ground truth queries.
        
        Args:
            task: The SQL task being evaluated
            response: The agent's SQL response
            
        Returns:
            EvaluationResult containing the evaluation outcome
        """
        # Cast to SQLTask to access database_path
        sql_task = task if isinstance(task, SQLTask) else SQLTask(
            query=task.query,
            ground_truth=task.ground_truth,
            database_path=task.metadata.get('database_path') if task.metadata else None
        )
        
        try:
            # Validate SQL syntax first
            if not self._validate_sql_syntax(response):
                return EvaluationResult(
                    success=False,
                    score=0.0,
                    error="Invalid SQL syntax",
                    details={"reason": "Invalid SQL syntax"}
                )
            
            # Execute the agent's SQL query
            agent_result = self._execute_query(response, sql_task.database_path)
            
            # Execute the ground truth SQL query if available
            if sql_task.ground_truth:
                ground_truth_result = self._execute_query(sql_task.ground_truth, sql_task.database_path)
                
                # Compare results
                success = self._compare_results(agent_result, ground_truth_result)
                score = 1.0 if success else 0.0
                
                return EvaluationResult(
                    success=success,
                    score=score,
                    details={
                        "agent_result": agent_result,
                        "ground_truth_result": ground_truth_result,
                        "comparison_method": "exact_match"
                    }
                )
            else:
                # If no ground truth, just verify the query executes without error
                return EvaluationResult(
                    success=True,
                    score=1.0,
                    details={
                        "agent_result": agent_result,
                        "reason": "Query executed successfully (no ground truth to compare)"
                    }
                )
                
        except Exception as e:
            return EvaluationResult(
                success=False,
                score=0.0,
                error=str(e),
                details={"exception_type": type(e).__name__}
            )
    
    def _validate_sql_syntax(self, sql: str) -> bool:
        """
        Validate SQL syntax without executing.
        
        Args:
            sql: SQL query to validate
            
        Returns:
            True if syntax appears valid, False otherwise
        """
        # Basic validation - in practice, this might use a SQL parser
        sql = sql.strip().upper()
        
        # Check for basic SQL structure
        if not (sql.startswith("SELECT") or sql.startswith("INSERT") or 
                sql.startswith("UPDATE") or sql.startswith("DELETE") or
                sql.startswith("WITH")):
            return False
            
        # Check for balanced quotes
        single_quotes = sql.count("'") - sql.count("''")  # Account for escaped quotes
        double_quotes = sql.count('"') - sql.count('""')
        
        if single_quotes % 2 != 0 or double_quotes % 2 != 0:
            return False
            
        return True
    
    def _execute_query(self, sql: str, database_path: Optional[str]) -> List[Dict[str, Any]]:
        """
        Execute a SQL query against the database.
        
        Args:
            sql: SQL query to execute
            database_path: Path to the SQLite database
            
        Returns:
            List of result rows as dictionaries
        """
        if not database_path:
            raise ValueError("Database path is required for query execution")
        
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        cursor = conn.cursor()
        
        # Set a timeout
        conn.execute("PRAGMA busy_timeout = 5000")  # 5 second timeout for lock acquisition
        
        try:
            start_time = time.time()
            cursor.execute(sql)
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Fetch all results
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            result = []
            for row in rows:
                result_dict = {}
                for i, col in enumerate(columns):
                    result_dict[col] = row[i]
                result.append(result_dict)
                
            execution_time = time.time() - start_time
            
            # Check timeout
            if execution_time > self.timeout:
                raise TimeoutError(f"Query execution exceeded {self.timeout} second timeout")
                
            return result
        finally:
            conn.close()
    
    def _compare_results(self, result1: List[Dict[str, Any]], result2: List[Dict[str, Any]]) -> bool:
        """
        Compare two sets of query results for equality.
        
        Args:
            result1: First result set
            result2: Second result set
            
        Returns:
            True if results are equivalent, False otherwise
        """
        if len(result1) != len(result2):
            return False
        
        # For simplicity, we're comparing exact matches
        # In a more sophisticated implementation, you might want to handle
        # different ordering, floating point precision, etc.
        return result1 == result2
    
    def supports_token_level_evaluation(self) -> bool:
        """
        Check if this evaluator supports token-level evaluation.
        
        Returns:
            True if token-level evaluation is supported, False otherwise
        """
        # SQL evaluation is not token-level, but rather structural and execution-based
        return False


class TextToSQLEnvironment(BaseEnvironment):
    """
    Text-to-SQL environment implementation for evaluating text-to-SQL agents.
    
    This environment provides Spider 2.0 integration and SQL execution validation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Text-to-SQL environment.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.task_generator = Spider2TaskGenerator(config or {})
        self.task_evaluator = SQLTaskEvaluator(config or {})
    
    def initialize(self):
        """
        Initialize the environment and its resources.
        """
        # Any setup needed for the environment
        print("Text-to-SQL environment initialized")
    
    def cleanup(self):
        """
        Clean up environment resources.
        """
        # Any cleanup needed for the environment
        print("Text-to-SQL environment cleaned up")
    
    def get_task_generator(self) -> Spider2TaskGenerator:
        """
        Get the task generator for this environment.
        
        Returns:
            TaskGenerator instance
        """
        return self.task_generator
    
    def get_task_evaluator(self) -> SQLTaskEvaluator:
        """
        Get the task evaluator for this environment.
        
        Returns:
            TaskEvaluator instance
        """
        return self.task_evaluator