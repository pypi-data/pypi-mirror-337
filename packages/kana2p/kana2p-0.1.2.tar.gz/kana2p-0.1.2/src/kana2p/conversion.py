"""
This module provides functions for converting between Katakana strings and
their corresponding phoneme representations.

The conversion is based on mapping dictionaries imported from `kana2p.const`.

Mappings:
    - KANA2PHONEME_MAP: Maps Katakana characters/sequences to lists of phonemes.
    - PHONEME2KANA_MAP: Maps tuples of phonemes back to the corresponding Katakana.
"""

import re
from typing import List

from kana2p.const import (
    BACKWARD_ADDITIONAL,
    FORWARD_ADDITIONAL,
    KANA2PHONEME_BIJECTION,
)

# -----------------------------------------------------------------------------
# Build mapping dictionaries
# -----------------------------------------------------------------------------

# Merge the bi-directional mapping and the additional forward mapping to create
# a dictionary for Katakana-to-phoneme conversion.
KANA2PHONEME_MAP = {**KANA2PHONEME_BIJECTION, **FORWARD_ADDITIONAL}

# Create the inverse mapping for phoneme-to-Katakana conversion.
# This is done by inverting KANA2PHONEME_BIJECTION and then updating with
# any additional backward mappings.
PHONEME2KANA_MAP = {
    **{v: k for k, v in KANA2PHONEME_BIJECTION.items()},
    **BACKWARD_ADDITIONAL,
}

# -----------------------------------------------------------------------------
# Prepare regular expression patterns for tokenization
# -----------------------------------------------------------------------------

# Sort the keys by length in descending order to ensure longer patterns match first.
_sorted_kana_keys = sorted(KANA2PHONEME_MAP.keys(), key=len, reverse=True)

# Compile a regex pattern that matches any of the mapped Katakana sequences.
# The pattern includes:
#   - All keys from KANA2PHONEME_MAP (properly escaped),
#   - The prolonged sound mark "ー",
#   - And any single character (as a fallback).
_kana2p_pattern = re.compile(
    "|".join(re.escape(k) for k in _sorted_kana_keys) + "|ー|."
)

# Prepare a sorted list of unique phoneme tokens from the bi-directional mapping.
# Tokens are sorted by length in descending order to facilitate greedy matching.
phoneme_tokens = sorted(
    {token for seq in KANA2PHONEME_BIJECTION.values() for token in seq},
    key=len,
    reverse=True,
)


# -----------------------------------------------------------------------------
# Conversion Functions
# -----------------------------------------------------------------------------


def katakana2phonemes(text: str, normalize: bool = False) -> List[str]:
    """
    Convert a Katakana string to a list of phonemes.

    The conversion is based on a predefined mapping of full-width Katakana characters
    to phonemes. Special cases include:
      - The sokuon "ッ" is converted to the phoneme "q".
      - The prolonged sound mark "ー" is converted to the phoneme ":".
      - The syllabic nasal "ン" is converted to the phoneme "N".
      - "ヲ" is converted to ["o"] rather than ["w", "o"].
      - "ヶ" is converted to ["k", "a"] rather than ["k", "e"].

    Note:
      - Only full-width Katakana are processed.
      - If a character is not found in the mapping and normalize is False,
        the character is passed through unchanged.
      - If normalize is True, characters not present in the mapping
        (e.g., non-Katakana characters) are excluded.

    Examples:
        "ハローー" → ["h", "a", "r", "o", ":", ":"]
        "グァヴァォ" → ["gw", "a", "v", "a", "o"]

    Args:
        text (str): The input Katakana string.
        normalize (bool): If True, exclude characters not found in the mapping.

    Returns:
        List[str]: A list of phoneme tokens.
    """
    result: List[str] = []
    # Iterate through all matches in the input text using the regex pattern.
    for m in _kana2p_pattern.finditer(text):
        token = m.group(0)
        if token in KANA2PHONEME_MAP:
            # Extend the result list with the phoneme sequence for the token.
            result.extend(KANA2PHONEME_MAP[token])
        else:
            # If normalization is off, include the token as-is.
            if not normalize:
                result.append(token)
    return result


def phonemes2katakana(phonemes: List[str]) -> str:
    """
    Convert a list of phonemes back to a Katakana string.

    The conversion is performed using a greedy matching algorithm that
    attempts to match the longest possible sequence of phonemes in the mapping.

    Example:
        ["ky", "a", "i"] → "キャイ"

    Args:
        phonemes (List[str]): The input list of phoneme tokens.

    Returns:
        str: The resulting Katakana string.
    """
    result = []
    i = 0
    n = len(phonemes)
    # Process the phoneme list from start to finish.
    while i < n:
        found = False
        # Attempt to match the longest sequence starting at index i.
        for j in range(n, i, -1):
            seq = tuple(phonemes[i:j])
            if seq in PHONEME2KANA_MAP:
                result.append(PHONEME2KANA_MAP[seq])
                i = j
                found = True
                break
        # If no matching sequence is found, append the current token as-is.
        if not found:
            result.append(phonemes[i])
            i += 1
    return "".join(result)
