"""OCR parser for extracting vocabulary from images using OpenAI Vision API.

This module provides the OpenAIVisionParser class for processing images
and extracting Japanese-German vocabulary with structured data.
"""

import base64
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class OpenAIVisionParser:
    """Parser that uses OpenAI Vision API to extract vocabulary from images.

    Extracts Japanese-German vocabulary pairs from images and returns
    structured data including vocab type, base forms, and translations.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OCR parser with OpenAI API key.

        Args:
            api_key: OpenAI API key (if None, loads from OPENAI_API_KEY env var)

        Raises:
            ImportError: If openai package is not installed
            ValueError: If API key is not provided or found in environment
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package is required for OCR functionality. "
                "Install it with: pip install openai"
            )

        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Either pass it to the constructor "
                "or set the OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)

    def extract_vocabulary_from_image(self, image_path: Path) -> List[Dict]:
        """Extract vocabulary items from an image using OpenAI Vision API.

        Args:
            image_path: Path to the image file

        Returns:
            List of dictionaries with keys:
            - japanese: List[str] - Japanese words/phrases
            - german: List[str] - German translations
            - vocab_type: str - 'noun', 'adjective', or 'pattern'
            - base_form: Optional[str] - Base form if word is conjugated

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image processing fails or response is invalid
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Read and encode image to base64
        image_base64 = self._encode_image(image_path)

        # Call OpenAI Vision API
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using GPT-4 Turbo with vision
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Japanese-German vocabulary extraction assistant. Extract vocabulary from images and return structured JSON data."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self._build_vision_prompt()
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.1  # Low temperature for more consistent extraction
            )

            # Extract and parse response
            content = response.choices[0].message.content

            # Try to extract JSON from response (might be wrapped in markdown code blocks)
            extracted_items = self._parse_json_response(content)

            return extracted_items

        except Exception as e:
            raise ValueError(f"Failed to extract vocabulary from image: {e}") from e

    def _encode_image(self, image_path: Path) -> str:
        """Encode image to base64 string.

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _build_vision_prompt(self) -> str:
        """Build the prompt for OpenAI Vision API.

        Returns:
            Prompt string with instructions for vocabulary extraction
        """
        return """
Extract all Japanese-German vocabulary from this image.

CRITICAL: Use the EXACT Japanese writing as shown in the image:
- If the image shows Hiragana (ひらがな), extract it as Hiragana
- If the image shows Katakana (カタカナ), extract it as Katakana
- If the image shows Kanji (漢字), extract it as Kanji
- DO NOT convert between scripts! Keep the exact characters you see!

For each vocabulary item, provide:
1. Japanese word(s)/phrase(s) - EXACTLY as written in the image
2. German translation(s) (can be multiple meanings)
3. Vocabulary type: "noun", "adjective", or "pattern"
4. Base form (optional): If conjugated/declined

SENTENCE PATTERNS:
- Patterns with placeholders like "[Ort] に [N] があります" should be extracted as vocab_type "pattern"
- Keep placeholders in square brackets exactly as shown
- Example: {"japanese": ["[Ort] に [N] があります"], "german": ["Es gibt [N] in [Ort]"], "vocab_type": "pattern"}

Return ONLY a JSON array with this exact format (no additional text or markdown):
[
  {
    "japanese": ["word1", "word2"],
    "german": ["translation1", "translation2"],
    "vocab_type": "noun",
    "base_form": "base form if applicable",
    "uncertain": false
  },
  {
    "japanese": ["できます"],
    "german": ["können", "schaffen"],
    "vocab_type": "pattern",
    "base_form": "できる",
    "uncertain": false
  },
  {
    "japanese": ["[Ort] に [N] があります"],
    "german": ["Es gibt [N] in [Ort]"],
    "vocab_type": "pattern",
    "uncertain": false
  },
  {
    "japanese": ["スパラシド"],
    "german": ["Spaßbad"],
    "vocab_type": "noun",
    "uncertain": true
  }
]

Important:
- NEVER convert between Hiragana/Katakana/Kanji - extract EXACTLY as shown!
- Always return valid JSON
- japanese and german must be arrays of strings
- vocab_type must be exactly "noun", "adjective", or "pattern"
- base_form is optional (omit or set to null if not applicable)
- "uncertain" field: Set to true if the handwriting is unclear or you're unsure about the extraction
- Include ALL vocabulary items AND sentence patterns visible in the image

UNCERTAINTY GUIDELINES:
- If handwriting is messy or unclear → uncertain: true
- If you can't read all characters clearly → uncertain: true
- If german translation is missing or unclear → uncertain: true
- If you're confident about the extraction → uncertain: false
""".strip()

    def _parse_json_response(self, response_content: str) -> List[Dict]:
        """Parse JSON response from OpenAI, handling markdown code blocks.

        Args:
            response_content: Raw response content from OpenAI

        Returns:
            Parsed list of vocabulary dictionaries

        Raises:
            ValueError: If response is not valid JSON or has wrong structure
        """
        # Remove markdown code blocks if present
        content = response_content.strip()

        # Try to extract JSON from markdown code blocks
        if content.startswith("```"):
            # Find the content between ```json and ```
            lines = content.split('\n')
            json_lines = []
            in_code_block = False

            for line in lines:
                if line.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    json_lines.append(line)

            content = '\n'.join(json_lines)

        # Parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Response is not valid JSON: {e}") from e

        # Validate structure
        if not isinstance(data, list):
            raise ValueError("Response must be a JSON array")

        # Validate each item
        validated_items = []
        for item in data:
            if not isinstance(item, dict):
                continue

            # Ensure required fields
            if 'japanese' not in item or 'german' not in item:
                continue

            # Ensure lists
            if not isinstance(item['japanese'], list):
                item['japanese'] = [item['japanese']]
            if not isinstance(item['german'], list):
                item['german'] = [item['german']]

            # Validate vocab_type
            if 'vocab_type' not in item or item['vocab_type'] not in ('noun', 'adjective', 'pattern'):
                item['vocab_type'] = 'noun'  # Default to noun

            # Handle base_form
            if 'base_form' not in item or item['base_form'] in (None, ''):
                item['base_form'] = None

            # Handle uncertain flag
            if 'uncertain' not in item or not isinstance(item['uncertain'], bool):
                item['uncertain'] = False  # Default to confident

            validated_items.append(item)

        return validated_items
