"""
Base classes for context system.

This module defines the fundamental abstract base classes for the Context system
that will support DBT, GraphRAG, and other semantic layer integrations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


@dataclass
class ContextElement:
    """
    Represents a single element in a context system.
    
    Attributes:
        id: Unique identifier for the context element
        type: Type of context (e.g., 'semantic_model', 'table_documentation', 'column_description')
        content: The actual context content
        metadata: Additional metadata about the context element
        relevance: Estimated relevance/importance score (0.0-1.0)
    """
    id: str
    type: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    relevance: float = 1.0


class BaseContextSystem(ABC):
    """
    Abstract base class for all context systems in the Semiosis framework.
    
    This class provides the core interface for different context providers
    including DBT, GraphRAG, and custom semantic layers.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the context system with configuration.
        
        Args:
            config: Configuration dictionary containing context-specific parameters
        """
        self.config = config
        
    def initialize(self):
        """
        Initialize the context system and its resources.
        """
        pass
    
    def cleanup(self):
        """
        Clean up context system resources.
        """
        pass
        
    @abstractmethod
    def extract_context(self) -> List[ContextElement]:
        """
        Extract all available context elements from the system.
        
        Returns:
            List of ContextElement objects
        """
        pass
    
    @abstractmethod
    def filter_context(self, query: str, max_elements: Optional[int] = None) -> List[ContextElement]:
        """
        Filter context elements relevant to a specific query.
        
        Args:
            query: The query to match against context
            max_elements: Maximum number of elements to return (None for no limit)
            
        Returns:
            List of relevant ContextElement objects
        """
        pass
    
    @abstractmethod
    def get_context_size(self) -> int:
        """
        Get the total number of available context elements.
        
        Returns:
            Total count of context elements
        """
        pass
    
    def get_context_string(self, elements: List[ContextElement]) -> str:
        """
        Convert context elements to a string representation suitable for agent input.
        
        Args:
            elements: List of context elements to convert
            
        Returns:
            String representation of the context
        """
        return "\n".join([elem.content for elem in elements])


class BaseIntervention(ABC):
    """
    Abstract base class for context interventions.
    
    Interventions modify context in systematic ways to measure their impact
    on agent performance using semantic information theory.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the intervention with configuration.
        
        Args:
            config: Configuration dictionary containing intervention-specific parameters
        """
        self.config = config
        self.noise_level = config.get('noise_level', 0.0)  # Level of intervention (0.0-1.0)
        
    @abstractmethod
    def apply(self, context: List[ContextElement]) -> List[ContextElement]:
        """
        Apply the intervention to the context elements.
        
        Args:
            context: Original list of context elements
            
        Returns:
            Modified list of context elements
        """
        pass
    
    @abstractmethod
    def revert(self, context: List[ContextElement]) -> List[ContextElement]:
        """
        Revert the intervention to restore original context (if possible).
        
        Args:
            context: Context elements that were modified by this intervention
            
        Returns:
            Original context elements (if revertible)
        """
        pass
    
    def get_noise_level(self) -> float:
        """
        Get the noise level of this intervention.
        
        Returns:
            Noise level (0.0-1.0) indicating the strength of the intervention
        """
        return self.noise_level