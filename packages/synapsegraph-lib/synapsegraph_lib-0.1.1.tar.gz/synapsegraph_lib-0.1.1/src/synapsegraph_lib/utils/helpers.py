"""
Helper utilities for the Synapse application.

This module provides common utility functions used across the application.
"""

import logging
import datetime
from typing import Dict, List, Optional, Any, Union, Set, Tuple
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_env_vars(env_file: Optional[str] = None) -> bool:
    """
    Load environment variables from .env file.

    Args:
        env_file: Path to .env file (if None, looks in current directory and parent directories)

    Returns:
        True if successful, False otherwise
    """
    try:
        if env_file:
            # Load from specified file
            if not os.path.exists(env_file):
                logger.error(f"Environment file not found: {env_file}")
                return False

            load_dotenv(env_file)
            logger.info(f"Loaded environment variables from {env_file}")
            return True
        else:
            # Try to find .env file in current directory or parent directories
            env_path = find_dotenv()
            if env_path:
                load_dotenv(env_path)
                logger.info(f"Loaded environment variables from {env_path}")
                return True
            else:
                logger.warning("No .env file found")
                return False
    except Exception as e:
        logger.error(f"Failed to load environment variables: {str(e)}")
        return False


def find_dotenv() -> Optional[str]:
    """
    Find .env file in current directory or parent directories.

    Returns:
        Path to .env file if found, None otherwise
    """
    current_dir = Path.cwd()

    # Check current directory
    env_path = current_dir / ".env"
    if env_path.exists():
        return str(env_path)

    # Check parent directories (up to 3 levels)
    for _ in range(3):
        current_dir = current_dir.parent
        env_path = current_dir / ".env"
        if env_path.exists():
            return str(env_path)

    return None


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """
    Set up logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (if None, logs to console only)
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    if log_file:
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(
            level=numeric_level,
            format=log_format,
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
    else:
        logging.basicConfig(level=numeric_level, format=log_format)

    logger.info(f"Logging initialized at level {log_level}")


def sanitize_cypher_input(input_str: str) -> str:
    """
    Sanitize input for Cypher queries to prevent injection attacks.

    Args:
        input_str: Input string to sanitize

    Returns:
        Sanitized string
    """
    # Replace single quotes with escaped single quotes
    sanitized = input_str.replace("'", "\\'")

    # Remove semicolons to prevent multiple statements
    sanitized = sanitized.replace(";", "")

    # Remove Cypher keywords that could be used for injection
    cypher_keywords = [
        "CREATE",
        "DELETE",
        "DETACH",
        "MATCH",
        "MERGE",
        "OPTIONAL",
        "REMOVE",
        "RETURN",
        "SET",
        "UNION",
        "UNWIND",
        "WITH",
    ]

    pattern = r"\b(" + "|".join(cypher_keywords) + r")\b"
    sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

    return sanitized


def calculate_confidence_decay(
    initial_confidence: float, age_days: int, decay_rate: float = 0.05
) -> float:
    """
    Calculate confidence decay based on age.

    Args:
        initial_confidence: Initial confidence value
        age_days: Age in days
        decay_rate: Daily decay rate

    Returns:
        Decayed confidence value
    """
    decay_factor = (1.0 - decay_rate) ** age_days
    decayed_confidence = initial_confidence * decay_factor

    # Ensure confidence doesn't go below a minimum threshold
    min_confidence = 0.1
    return max(decayed_confidence, min_confidence)


def apply_resistance_factor(
    old_value: float, new_value: float, resistance_factor: float = 0.8
) -> float:
    """
    Apply resistance factor to slow changes in values.

    Args:
        old_value: Old value
        new_value: New value
        resistance_factor: Resistance factor (0.0 to 1.0)

    Returns:
        Blended value
    """
    return old_value * resistance_factor + new_value * (1.0 - resistance_factor)


def extract_entities_simple(text: str) -> List[str]:
    """
    Simple entity extraction from text (for testing purposes).

    Args:
        text: Input text

    Returns:
        List of potential entity names
    """
    # This is a very simplified approach - in a real system, you would use
    # more sophisticated NLP techniques for entity extraction

    # Look for capitalized words that might be entities
    potential_entities = re.findall(r"\b[A-Z][a-z]+\b", text)

    # Remove duplicates
    return list(set(potential_entities))


def extract_statements_simple(text: str) -> List[str]:
    """
    Simple statement extraction from text (for testing purposes).

    Args:
        text: Input text

    Returns:
        List of potential statements
    """
    # Split text into sentences
    sentences = re.split(r"[.!?]+", text)

    # Filter out empty sentences and strip whitespace
    statements = [s.strip() for s in sentences if s.strip()]

    return statements


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.

    Args:
        file_path: Path to JSON file

    Returns:
        Dictionary with JSON data
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON file {file_path}: {str(e)}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: Data to save
        file_path: Path to save JSON file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        return True
    except Exception as e:
        logger.error(f"Failed to save JSON file {file_path}: {str(e)}")
        return False


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        Current timestamp string
    """
    return datetime.datetime.now().isoformat()


def parse_timestamp(timestamp_str: str) -> Optional[datetime.datetime]:
    """
    Parse timestamp string to datetime object.

    Args:
        timestamp_str: Timestamp string in ISO format

    Returns:
        Datetime object if successful, None otherwise
    """
    try:
        return datetime.datetime.fromisoformat(timestamp_str)
    except ValueError:
        logger.error(f"Failed to parse timestamp: {timestamp_str}")
        return None
