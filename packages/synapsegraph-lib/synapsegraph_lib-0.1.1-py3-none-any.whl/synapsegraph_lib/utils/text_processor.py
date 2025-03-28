"""
Text processor utility for SynapseGraph.

This module provides functionality for processing text before ingestion,
including splitting large texts into manageable chunks.
"""

import re
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class TextProcessor:
    """
    Text processor class for preparing text for ingestion.

    This class provides functionality for:
    1. Splitting large texts into manageable chunks
    2. Basic cleaning of text
    3. Identifying potential topic boundaries
    """

    def __init__(self, max_chunk_size: int = 2000, overlap: int = 100):
        """
        Initialize the TextProcessor.

        Args:
            max_chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        self.max_chunk_size = max_chunk_size
        self.overlap = min(
            overlap, max_chunk_size // 5
        )  # Ensure overlap is not too large

    def clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace, normalizing line breaks, etc.

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        # Skip if text is already small
        if len(text) < 1000:
            return text

        # Remove excess whitespace
        text = re.sub(r"\s+", " ", text)

        # Normalize line breaks
        text = re.sub(r"[\r\n]+", "\n", text)

        # Remove any non-printable characters
        text = re.sub(r"[^\x20-\x7E\n]", "", text)

        return text.strip()

    def split_text(self, text: str) -> List[str]:
        """
        Split text into manageable chunks.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        # Performance optimization - track timing
        import time

        start_time = time.time()

        # If text is already small enough, return it as a single chunk
        if len(text) <= self.max_chunk_size:
            return [text]

        # Clean the text - skip for small texts
        if len(text) > 1000:
            cleaned_text = self.clean_text(text)
        else:
            cleaned_text = text

        # For very small texts, don't do complex splitting
        if len(cleaned_text) <= self.max_chunk_size:
            return [cleaned_text]

        chunks = []
        current_position = 0
        text_length = len(cleaned_text)

        # Add safety counter to prevent infinite loops
        max_iterations = 100  # This should be more than enough for any reasonable text
        iteration = 0

        # Faster splitting - prioritize speed over perfect chunks
        while current_position < text_length and iteration < max_iterations:
            iteration += 1

            # Determine end position for current chunk
            end_position = min(current_position + self.max_chunk_size, text_length)

            # Try to find a good breakpoint (period, paragraph, etc)
            if end_position < text_length:
                # Simple search for period followed by space, prioritizing speed
                boundary_idx = cleaned_text.rfind(". ", current_position, end_position)
                if boundary_idx > current_position + (self.max_chunk_size // 2):
                    end_position = boundary_idx + 2  # Include the period and space

            # Extract the chunk
            chunk = cleaned_text[current_position:end_position].strip()
            if chunk:  # Ensure we don't add empty chunks
                chunks.append(chunk)

            # IMPORTANT FIX: Move to next position - ensure we're actually advancing
            old_position = current_position
            current_position = end_position - self.overlap

            # Safety check: Make sure we're advancing in the text
            if current_position <= old_position:
                logger.warning(
                    f"Position not advancing ({current_position} <= {old_position}). Forcing advancement."
                )
                current_position = old_position + max(
                    self.overlap, 100
                )  # Force moving forward

            # Additional safety - if we're near the end, just finish
            if text_length - current_position < self.overlap * 2:
                current_position = text_length

        # Check if we hit the iteration limit - this indicates a potential problem
        if iteration >= max_iterations:
            logger.warning(
                f"Text splitting reached max iterations ({max_iterations}). Check for potential infinite loop."
            )

        elapsed = time.time() - start_time
        logger.debug(f"Split text into {len(chunks)} chunks in {elapsed:.3f} seconds")
        return chunks

    def extract_potential_topics(self, text: str, max_topics: int = 5) -> List[str]:
        """
        Extract potential topics from text.

        Args:
            text: Text to analyze
            max_topics: Maximum number of topics to extract

        Returns:
            List of potential topics
        """
        # This is a very simple implementation that looks for capitalized phrases
        # and frequently occurring terms. In a real implementation, you might use
        # NLP techniques like TF-IDF, NER, or topic modeling.

        # Look for capitalized phrases that might be topics
        capitalized_pattern = r"[A-Z][a-z]{2,}\s+(?:[A-Z][a-z]+\s+){0,3}[A-Z][a-z]+"
        capitalized_matches = re.findall(capitalized_pattern, text)

        # Count word frequency (simple approach)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
        word_counts = {}
        for word in words:
            if word not in ("this", "that", "with", "from", "have", "about", "which"):
                word_counts[word] = word_counts.get(word, 0) + 1

        # Get most frequent words
        frequent_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[
            :max_topics
        ]

        # Combine the results
        topics = set()
        for phrase in capitalized_matches[:max_topics]:
            topics.add(phrase.strip())

        for word, count in frequent_words:
            if count > 2:  # Only include if it appears multiple times
                topics.add(word)

        return list(topics)[:max_topics]
