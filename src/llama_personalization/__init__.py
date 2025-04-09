"""
LlamaPersonalization - Toolkit for personalized experiences.
"""

from .core import PersonalizationClient
from .config import PersonalizationConfig
from .types import UserProfile, RecommendationResult # Import from types.py
# Placeholder types - consider moving to a types.py if complex - REMOVED
# from .core import UserProfile, RecommendationResult 
# Engine is internal for now
# from .engine import PersonalizationEngine 

__version__ = "0.1.0" # Keep version at 0.1.0 for now

__all__ = [
    "PersonalizationClient",
    "PersonalizationConfig",
    "UserProfile",             # Export placeholder type
    "RecommendationResult",    # Export placeholder type
]
