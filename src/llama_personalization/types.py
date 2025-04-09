"""
Type definitions for LlamaPersonalization data structures.
"""

from typing import TypedDict, List, Dict, Any, Optional

class RecommendationItem(TypedDict):
    """Represents a single recommended item."""
    item_id: str
    score: float
    type: Optional[str] # e.g., 'article', 'product'
    # Add other relevant fields like title, description, url later

class RecommendationResult(TypedDict):
    """Represents the result of a recommendation request."""
    user_id: str
    items: List[RecommendationItem]
    engine_info: Optional[str] # Information about the engine/model used
    error: Optional[str] # Error message if the request failed

class UserProfile(TypedDict):
    """Represents a user profile.
    
    This is a basic structure. Could include more complex fields like:
    - embeddings: Dict[str, List[float]]
    - interaction_history: List[Dict]
    - demographic_info: Dict
    """
    user_id: str
    interests: Optional[List[str]] # e.g., ["ai", "python", "webdev"]
    preferences: Optional[Dict[str, Any]] # e.g., {"content_length": "short", "preferred_topics": ["ml"]}
    # Add other profile fields as needed 