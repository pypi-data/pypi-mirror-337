"""
Configuration module for managing application settings.

This module provides a centralized configuration system for the Synapse application,
supporting environment variables, configuration files, and default values.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json

from synapsegraph_lib.utils.helpers import load_env_vars

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_env_vars()


class SourceType(str, Enum):
    """Enumeration of possible source types for knowledge ingestion."""

    USER = "User"
    RESEARCH = "Research"
    NEWS = "News"
    API = "API"
    FILE = "File"


class OpinionStance(str, Enum):
    """Enumeration of possible stances for opinions."""

    SUPPORTIVE = "Supportive"
    OPPOSED = "Opposed"
    MIXED = "Mixed"
    NEUTRAL = "Neutral"


class ConflictStatus(str, Enum):
    """Enumeration of possible statuses for conflict resolution."""

    ACTIVE = "Active"
    RESOLVED = "Resolved"


class TimeHorizon(str, Enum):
    """Enumeration of possible time horizons for opinions."""

    SHORT_TERM = "Short-term"
    MEDIUM_TERM = "Medium-term"
    LONG_TERM = "Long-term"
    UNKNOWN = "Unknown"

    @classmethod
    def from_string(cls, value: str) -> "TimeHorizon":
        """
        Convert a string to a TimeHorizon enum value.

        Args:
            value: String value to convert

        Returns:
            TimeHorizon enum value
        """
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN


@dataclass
class DatabaseConfig:
    """Configuration for database connections."""

    uri: str = field(
        default_factory=lambda: os.getenv("NEO4J_URI", "bolt://localhost:7687")
    )
    username: str = field(default_factory=lambda: os.getenv("NEO4J_USERNAME", "neo4j"))
    password: str = field(
        default_factory=lambda: os.getenv("NEO4J_PASSWORD", "password")
    )
    database: Optional[str] = field(
        default_factory=lambda: os.getenv("NEO4J_DATABASE", None)
    )


@dataclass
class LLMConfig:
    """Configuration for LLM integration."""

    provider: str = field(default_factory=lambda: os.getenv("LLM_PROVIDER", "openai"))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o"))
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    temperature: float = field(
        default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.7"))
    )
    max_tokens: int = field(
        default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "1000"))
    )


@dataclass
class SynapseConfig:
    """Main configuration for the Synapse application."""

    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)

    # Opinion formation settings
    min_confidence_threshold: float = field(
        default_factory=lambda: float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.3"))
    )
    opinion_resistance_factor: float = field(
        default_factory=lambda: float(os.getenv("OPINION_RESISTANCE_FACTOR", "0.8"))
    )
    confidence_decay_rate: float = field(
        default_factory=lambda: float(os.getenv("CONFIDENCE_DECAY_RATE", "0.05"))
    )
    min_opinion_clarity_threshold: float = field(
        default_factory=lambda: float(os.getenv("MIN_OPINION_CLARITY_THRESHOLD", "0.6"))
    )

    # Source trust settings
    default_source_trust: float = field(
        default_factory=lambda: float(os.getenv("DEFAULT_SOURCE_TRUST", "0.5"))
    )
    min_source_trust: float = field(
        default_factory=lambda: float(os.getenv("MIN_SOURCE_TRUST", "0.3"))
    )

    # Conflict resolution settings
    contradiction_threshold: float = field(
        default_factory=lambda: float(os.getenv("CONTRADICTION_THRESHOLD", "0.7"))
    )

    # Logging settings
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    def __post_init__(self):
        """Set up logging based on configuration."""
        numeric_level = getattr(logging, self.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {self.log_level}")
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    @classmethod
    def from_file(cls, file_path: str) -> "SynapseConfig":
        """
        Load configuration from a JSON file.

        Args:
            file_path: Path to the JSON configuration file

        Returns:
            SynapseConfig instance
        """
        try:
            with open(file_path, "r") as f:
                config_data = json.load(f)

            # Create nested configs
            if "database" in config_data:
                config_data["database"] = DatabaseConfig(**config_data["database"])
            if "llm" in config_data:
                config_data["llm"] = LLMConfig(**config_data["llm"])

            return cls(**config_data)
        except Exception as e:
            logger.error(f"Failed to load configuration from {file_path}: {str(e)}")
            logger.info("Using default configuration")
            return cls()

    def to_file(self, file_path: str):
        """
        Save configuration to a JSON file.

        Args:
            file_path: Path to save the JSON configuration file
        """
        try:
            # Convert to dictionary
            config_dict = {
                "database": {
                    "uri": self.database.uri,
                    "username": self.database.username,
                    "password": self.database.password,
                    "database": self.database.database,
                },
                "llm": {
                    "provider": self.llm.provider,
                    "model": self.llm.model,
                    "api_key": self.llm.api_key,
                    "temperature": self.llm.temperature,
                    "max_tokens": self.llm.max_tokens,
                },
                "min_confidence_threshold": self.min_confidence_threshold,
                "opinion_resistance_factor": self.opinion_resistance_factor,
                "confidence_decay_rate": self.confidence_decay_rate,
                "min_opinion_clarity_threshold": self.min_opinion_clarity_threshold,
                "default_source_trust": self.default_source_trust,
                "min_source_trust": self.min_source_trust,
                "contradiction_threshold": self.contradiction_threshold,
                "log_level": self.log_level,
            }

            with open(file_path, "w") as f:
                json.dump(config_dict, f, indent=4)

            logger.info(f"Configuration saved to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save configuration to {file_path}: {str(e)}")


# Create a global configuration instance
config = SynapseConfig()
