"""
Japanese vocabulary database.

This module provides a complete list of Japanese vocabulary words,
including their Romaji transcriptions and German translations, based on the Word domain model.
This file maintains backward compatibility by combining basic and advanced words.
"""

from typing import List
from nihon_cli.core.word import Word
from nihon_cli.data.words_basic import WORDS_BASIC
from nihon_cli.data.words_advanced import WORDS_ADVANCED

# Combine basic and advanced words for backward compatibility
WORDS: List[Word] = WORDS_BASIC + WORDS_ADVANCED


def get_words(include_advanced: bool = True) -> List[Word]:
    """
    Get all Japanese vocabulary words (basic + advanced combined).

    Args:
        include_advanced (bool): Deprecated parameter, kept for backward compatibility.
                                Always returns all words (basic + advanced).

    Returns:
        List[Word]: List of all Japanese vocabulary words.
    """
    # Always return all words (basic + advanced) for the unified words mode
    return WORDS_BASIC + WORDS_ADVANCED


def get_words_by_category(category: str, include_advanced: bool = True) -> List[Word]:
    """
    Get Japanese vocabulary words filtered by category.

    Args:
        category (str): The category to filter by (e.g., 'animals', 'food').
        include_advanced (bool): Deprecated parameter, kept for backward compatibility.

    Returns:
        List[Word]: List of words in the specified category.
    """
    all_words = get_words()
    return [word for word in all_words if word.category == category]


def get_available_categories(include_advanced: bool = True) -> List[str]:
    """
    Get all available word categories.

    Args:
        include_advanced (bool): Deprecated parameter, kept for backward compatibility.

    Returns:
        List[str]: Sorted list of unique categories.
    """
    all_words = get_words()
    categories = set(word.category for word in all_words)
    return sorted(categories)


def get_word_count(include_advanced: bool = True) -> int:
    """
    Get the total number of words available.

    Args:
        include_advanced (bool): Deprecated parameter, kept for backward compatibility.

    Returns:
        int: Total number of words.
    """
    return len(get_words())


def get_category_counts(include_advanced: bool = True) -> dict[str, int]:
    """
    Get word counts per category.

    Args:
        include_advanced (bool): Deprecated parameter, kept for backward compatibility.

    Returns:
        dict[str, int]: Dictionary mapping category names to word counts.
    """
    all_words = get_words()
    category_counts = {}
    for word in all_words:
        category_counts[word.category] = category_counts.get(word.category, 0) + 1
    return category_counts