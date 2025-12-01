"""
Context system for Semiosis.

This package provides the protocol and tools for integrating various context
sources (DBT, file systems, etc.) into agent evaluations.
"""

from .interventions import (
    apply_intervention,
    compose_interventions,
    remove_percentage,
    shuffle_content,
    truncate_context,
)
from .protocol import ContextProvider
from .providers import DBTContextSystem

__all__ = [
    "ContextProvider",
    "DBTContextSystem",
    "apply_intervention",
    "remove_percentage",
    "shuffle_content",
    "truncate_context",
    "compose_interventions",
]
