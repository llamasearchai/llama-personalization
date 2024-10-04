"""
llama_personalization
====================

A privacy-focused personalization engine for language models that uses federated learning,
differential privacy, secure enclaves, and homomorphic encryption.
"""

__version__ = "0.1.0"

from .agent import Agent
from .config import (
    Config,
    ConfigError,
    FederatedConfig,
    ModelConfig,
    PrivacyConfig,
    SecurityConfig,
)
from .core_ml import CoreMLPrivateInterface
from .differential_privacy import DifferentialPrivacy
from .explainable_recommender import ExplainableRecommender
from .federated_learning import FederatedLearningEnv
from .homomorphic_encryption import MLXHomomorphicEncryption
from .lora_adapter import LoRAAdapter
from .personalization_engine import PersonalizationEngine
from .secure_enclave import SecureEnclaveSimulation

__all__ = [
    "Config",
    "PrivacyConfig",
    "FederatedConfig",
    "ModelConfig",
    "SecurityConfig",
    "ConfigError",
    "SecureEnclaveSimulation",
    "DifferentialPrivacy",
    "MLXHomomorphicEncryption",
    "CoreMLPrivateInterface",
    "LoRAAdapter",
    "FederatedLearningEnv",
    "Agent",
    "ExplainableRecommender",
    "PersonalizationEngine",
]
