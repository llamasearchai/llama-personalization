"""
Configuration management for LlamaPersonalization.
"""
from typing import Dict, Any, Optional
import logging # Use logging instead of print for errors potentially

logger = logging.getLogger(__name__)

class PersonalizationConfig:
    """Handles configuration for the personalization system with defaults."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "engine": {
            "model_type": "placeholder", # e.g., collaborative_filtering, content_based
            "default_num_recommendations": 10,
        },
        "profile_store": {
             "type": "memory", # e.g., memory, redis, database
             "max_size": 10000, # Example if using in-memory store
        },
        "logging": {
             "log_level": "INFO",
             "log_file": None, # e.g., "/var/log/personalization.log"
        }
    }

    def __init__(self, config_overrides: Optional[Dict[str, Any]] = None):
        """Initialize with optional configuration overrides.

        Overrides are deeply merged with the default configuration.
        """
        # Start with a deep copy of defaults to avoid modifying the class variable
        self.config = self._deep_copy(self.DEFAULT_CONFIG)
        if config_overrides:
            self._deep_merge(self.config, config_overrides)

    def _deep_copy(self, data: Any) -> Any:
        """Perform a basic deep copy for nested dicts/lists."""
        if isinstance(data, dict):
            return {k: self._deep_copy(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._deep_copy(elem) for elem in data]
        else:
            return data # Copies immutable types

    def _deep_merge(self, base: Dict, updates: Dict) -> None:
        """Recursively merge 'updates' dict into 'base' dict."""
        for key, value in updates.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_merge(base[key], value)
            else:
                 base[key] = value # Overwrites or adds new key

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation (e.g., 'engine.model_type')."""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                if isinstance(value, dict):
                    value = value[k]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default

    # Keep set method simple for now, only updates top-level or existing nested keys
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation (simplified)."""
        keys = key.split('.')
        current_level = self.config
        try:
            for i, k in enumerate(keys):
                if i == len(keys) - 1:
                    if isinstance(current_level, dict):
                        current_level[k] = value
                    else:
                        raise TypeError(f"Cannot set value at '{key}', intermediate path is not a dictionary.")
                elif isinstance(current_level, dict) and k in current_level:
                    current_level = current_level[k]
                else:
                    raise KeyError(f"Cannot set value at '{key}', key '{k}' not found or path invalid.")
        except (KeyError, TypeError) as e:
            logger.error(f"Error setting config key '{key}': {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Return a deep copy of the configuration dictionary."""
        return self._deep_copy(self.config)

    # Convenience access for log level
    @property
    def log_level(self) -> str:
         return self.get("logging.log_level", "INFO").upper()
