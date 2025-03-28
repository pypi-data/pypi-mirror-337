"""Utility functions for text sanitization to protect against HTML/JavaScript injection."""

from typing import Optional
import re
from bs4 import BeautifulSoup


def sanitize_text(text: Optional[str]) -> Optional[str]:
    """
    Sanitize text to remove HTML tags and JavaScript, returning plain text.
    Preserves all natural language characters including Cyrillic, CJK characters,
    and all punctuation marks.

    Args:
        text: Input text to sanitize

    Returns:
        Sanitized text with HTML/JavaScript removed but preserving all natural language characters
    """
    if text is None:
        return None

    # Use BeautifulSoup to parse and extract text
    soup = BeautifulSoup(text, 'html.parser')

    # Get text content, which removes all HTML tags
    clean_text = soup.get_text()

    # Remove any remaining script-like patterns
    clean_text = re.sub(r'javascript:', '', clean_text, flags=re.IGNORECASE)

    # Remove only control characters but preserve all printable characters
    # This keeps Cyrillic, CJK characters, and other non-Latin scripts intact
    clean_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', clean_text)

    return clean_text.strip()
