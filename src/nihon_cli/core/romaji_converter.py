# src/nihon_cli/core/romaji_converter.py
"""
Romaji to Kana conversion utilities.

This module provides functionality to convert romanized Japanese text (romaji)
to the corresponding Hiragana or Katakana characters.
"""

from typing import Dict, Optional
from nihon_cli.data.hiragana_basic import HIRAGANA_BASIC_CHARACTERS
from nihon_cli.data.hiragana_advanced import HIRAGANA_ADVANCED_CHARACTERS
from nihon_cli.data.katakana_basic import KATAKANA_BASIC_CHARACTERS
from nihon_cli.data.katakana_advanced import KATAKANA_ADVANCED_CHARACTERS


class RomajiConverter:
    """
    Converts romaji text to Hiragana or Katakana characters.
    
    This class builds mapping dictionaries from the existing character data
    and provides methods to convert romaji strings to their corresponding
    Japanese characters.
    """
    
    def __init__(self):
        """Initialize the converter with romaji-to-kana mappings."""
        self._hiragana_map: Dict[str, str] = {}
        self._katakana_map: Dict[str, str] = {}
        self._build_mappings()
    
    def _build_mappings(self) -> None:
        """
        Build romaji-to-kana mapping dictionaries from character data.
        """
        # Build Hiragana mapping
        all_hiragana = HIRAGANA_BASIC_CHARACTERS + HIRAGANA_ADVANCED_CHARACTERS
        for char in all_hiragana:
            self._hiragana_map[char.romaji] = char.symbol
        
        # Build Katakana mapping
        all_katakana = KATAKANA_BASIC_CHARACTERS + KATAKANA_ADVANCED_CHARACTERS
        for char in all_katakana:
            self._katakana_map[char.romaji] = char.symbol
    
    def romaji_to_hiragana(self, romaji: str) -> Optional[str]:
        """
        Convert romaji to Hiragana character.
        
        Args:
            romaji (str): The romaji string to convert.
            
        Returns:
            Optional[str]: The corresponding Hiragana character, or None if not found.
        """
        return self._hiragana_map.get(romaji.lower())
    
    def romaji_to_katakana(self, romaji: str) -> Optional[str]:
        """
        Convert romaji to Katakana character.
        
        Args:
            romaji (str): The romaji string to convert.
            
        Returns:
            Optional[str]: The corresponding Katakana character, or None if not found.
        """
        return self._katakana_map.get(romaji.lower())
    
    def romaji_to_kana(self, romaji: str, prefer_hiragana: bool = True) -> Optional[str]:
        """
        Convert romaji to either Hiragana or Katakana.
        
        Args:
            romaji (str): The romaji string to convert.
            prefer_hiragana (bool): If True, prefer Hiragana over Katakana.
                                   If False, prefer Katakana over Hiragana.
            
        Returns:
            Optional[str]: The corresponding Japanese character, or None if not found.
        """
        if prefer_hiragana:
            result = self.romaji_to_hiragana(romaji)
            if result is None:
                result = self.romaji_to_katakana(romaji)
            return result
        else:
            result = self.romaji_to_katakana(romaji)
            if result is None:
                result = self.romaji_to_hiragana(romaji)
            return result
    
    def convert_word_to_kana(self, romaji_word: str, prefer_hiragana: bool = True) -> Optional[str]:
        """
        Convert a romaji word to kana by breaking it into syllables.
        
        This method attempts to parse the romaji word into individual syllables
        and convert each to the corresponding kana character.
        
        Args:
            romaji_word (str): The romaji word to convert.
            prefer_hiragana (bool): If True, prefer Hiragana over Katakana.
            
        Returns:
            Optional[str]: The converted kana string, or None if conversion fails.
        """
        if not romaji_word:
            return None
            
        # First try direct conversion (for single syllables)
        direct_result = self.romaji_to_kana(romaji_word, prefer_hiragana)
        if direct_result:
            return direct_result
        
        # Try syllable-by-syllable conversion
        result = ""
        i = 0
        romaji_lower = romaji_word.lower()
        
        while i < len(romaji_lower):
            # Try longer syllables first (3 chars, then 2, then 1)
            found = False
            
            for length in [3, 2, 1]:
                if i + length <= len(romaji_lower):
                    syllable = romaji_lower[i:i + length]
                    kana = self.romaji_to_kana(syllable, prefer_hiragana)
                    if kana:
                        result += kana
                        i += length
                        found = True
                        break
            
            if not found:
                # If we can't convert this part, return None
                return None
        
        return result if result else None
    
    def convert_word_to_kana_safe(self, romaji_word: str, prefer_hiragana: bool = True) -> Optional[str]:
        """
        Convert a romaji word to kana, but only if it's not a valid word in the database.
        
        This method first checks if the romaji input corresponds to a valid Japanese word
        in the word database. If it does, it returns None to avoid showing incorrect kana.
        If it doesn't, it performs syllable-based conversion.
        
        Args:
            romaji_word (str): The romaji word to convert.
            prefer_hiragana (bool): If True, prefer Hiragana over Katakana.
            
        Returns:
            Optional[str]: The converted kana string, or None if word exists in DB or conversion fails.
        """
        if not romaji_word:
            return None
        
        # Check if this romaji corresponds to a word in the database
        try:
            from nihon_cli.data.words import get_words
            all_words = get_words(include_advanced=True)
            
            # If the romaji matches any word's romaji, don't convert (it's a real word)
            for word in all_words:
                if word.romaji.lower() == romaji_word.lower():
                    return None
        except ImportError:
            # If we can't import words, fall back to regular conversion
            pass
        
        # If it's not a real word, try syllable-based conversion
        return self.convert_word_to_kana(romaji_word, prefer_hiragana)


# Global converter instance
_converter = RomajiConverter()


def convert_romaji_to_hiragana(romaji: str) -> Optional[str]:
    """
    Convert romaji to Hiragana character.
    
    Args:
        romaji (str): The romaji string to convert.
        
    Returns:
        Optional[str]: The corresponding Hiragana character, or None if not found.
    """
    return _converter.romaji_to_hiragana(romaji)


def convert_romaji_to_katakana(romaji: str) -> Optional[str]:
    """
    Convert romaji to Katakana character.
    
    Args:
        romaji (str): The romaji string to convert.
        
    Returns:
        Optional[str]: The corresponding Katakana character, or None if not found.
    """
    return _converter.romaji_to_katakana(romaji)


def convert_romaji_to_kana(romaji: str, prefer_hiragana: bool = True) -> Optional[str]:
    """
    Convert romaji to either Hiragana or Katakana.
    
    Args:
        romaji (str): The romaji string to convert.
        prefer_hiragana (bool): If True, prefer Hiragana over Katakana.
                               If False, prefer Katakana over Hiragana.
        
    Returns:
        Optional[str]: The corresponding Japanese character, or None if not found.
    """
    return _converter.romaji_to_kana(romaji, prefer_hiragana)


def convert_romaji_word_to_kana(romaji_word: str, prefer_hiragana: bool = True) -> Optional[str]:
    """
    Convert a romaji word to kana by breaking it into syllables.
    
    Args:
        romaji_word (str): The romaji word to convert (e.g., "neko", "sakana").
        prefer_hiragana (bool): If True, prefer Hiragana over Katakana.
        
    Returns:
        Optional[str]: The corresponding kana string, or None if conversion fails.
    """
    return _converter.convert_word_to_kana(romaji_word, prefer_hiragana)