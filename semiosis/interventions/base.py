"""
Base classes for intervention system.

This module defines the fundamental abstract base classes for the Intervention system
that will support systematic context modifications for semantic information measurement.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from semiosis.contexts.base import ContextElement


class BaseIntervention(ABC):
    """
    Abstract base class for all interventions in the Semiosis framework.
    
    This class provides the core interface for different types of interventions
    that modify context in systematic ways to measure their impact on agent performance.
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