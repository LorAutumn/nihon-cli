"""Markdown parser for vocabulary tables.

This module provides functionality to parse Markdown files containing
vocabulary tables with Japanese and German translations.
"""

import re
from pathlib import Path
from typing import List, Tuple

from nihon_cli.core.vocabulary import VocabularyItem


class MarkdownVocabParser:
    """Parser for Markdown tables containing vocabulary entries.
    
    Expected format:
    | Japanisch | Deutsch |
    |-----------|---------|
    | こんにちは | Hallo, Guten Tag |
    | ありがとう | Danke |
    """
    
    # Regex pattern to match table rows (excluding header and separator)
    TABLE_ROW_PATTERN = re.compile(
        r'^\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$'
    )
    
    # Pattern to identify header row
    HEADER_PATTERN = re.compile(
        r'^\s*\|\s*Japanisch\s*\|\s*Deutsch\s*\|\s*$',
        re.IGNORECASE
    )
    
    # Pattern to identify separator row
    SEPARATOR_PATTERN = re.compile(
        r'^\s*\|[\s\-:]+\|[\s\-:]+\|\s*$'
    )
    
    @staticmethod
    def parse(file_path: Path) -> List[VocabularyItem]:
        """Parse a Markdown file and extract vocabulary items.
        
        Args:
            file_path: Path to the Markdown file to parse
            
        Returns:
            List of VocabularyItem objects parsed from the file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid or required columns are missing
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            raise ValueError(f"Failed to read file as UTF-8: {e}") from e
        
        # Parse the content
        vocab_pairs = MarkdownVocabParser._extract_vocab_pairs(content)
        
        if not vocab_pairs:
            raise ValueError(
                "No valid vocabulary entries found. "
                "Expected a table with 'Japanisch' and 'Deutsch' columns."
            )
        
        # Convert to VocabularyItem objects
        items = []
        for japanese, german in vocab_pairs:
            item = VocabularyItem(
                id=0,  # Will be set by database
                japanese_vocab=MarkdownVocabParser._split_multiple_meanings(japanese),
                german_vocab=MarkdownVocabParser._split_multiple_meanings(german),
                source_file=file_path.name,
                upload_tag="",  # Will be set by caller
                correct_german=0,
                correct_japanese=0,
                completed=False
            )
            items.append(item)
        
        return items
    
    @staticmethod
    def _extract_vocab_pairs(content: str) -> List[Tuple[str, str]]:
        """Extract vocabulary pairs from Markdown content.
        
        Args:
            content: The Markdown file content
            
        Returns:
            List of (japanese, german) tuples
        """
        lines = content.split('\n')
        vocab_pairs = []
        in_table = False
        header_found = False
        
        for line in lines:
            # Check for header row
            if MarkdownVocabParser.HEADER_PATTERN.match(line):
                header_found = True
                in_table = True
                continue
            
            # Check for separator row
            if in_table and MarkdownVocabParser.SEPARATOR_PATTERN.match(line):
                continue
            
            # If we're in a table and found the header, try to parse data rows
            if in_table and header_found:
                match = MarkdownVocabParser.TABLE_ROW_PATTERN.match(line)
                if match:
                    japanese = match.group(1).strip()
                    german = match.group(2).strip()
                    
                    # Skip empty rows
                    if japanese and german:
                        vocab_pairs.append((japanese, german))
                elif line.strip() and not line.strip().startswith('|'):
                    # End of table (non-table line encountered)
                    in_table = False
                    header_found = False
        
        return vocab_pairs
    
    @staticmethod
    def _split_multiple_meanings(text: str) -> List[str]:
        """Split comma-separated meanings into a list.
        
        Args:
            text: Text containing comma-separated meanings
            
        Returns:
            List of individual meanings, stripped of whitespace
        """
        return [item.strip() for item in text.split(',') if item.strip()]
    
    @staticmethod
    def validate_table_format(content: str) -> bool:
        """Validate that the content contains a properly formatted table.
        
        Args:
            content: The Markdown file content to validate
            
        Returns:
            True if the content contains a valid vocabulary table, False otherwise
        """
        lines = content.split('\n')
        
        # Check for header
        has_header = any(
            MarkdownVocabParser.HEADER_PATTERN.match(line) 
            for line in lines
        )
        
        if not has_header:
            return False
        
        # Check for at least one data row
        has_data = any(
            MarkdownVocabParser.TABLE_ROW_PATTERN.match(line) 
            and not MarkdownVocabParser.HEADER_PATTERN.match(line)
            and not MarkdownVocabParser.SEPARATOR_PATTERN.match(line)
            for line in lines
        )
        
        return has_data