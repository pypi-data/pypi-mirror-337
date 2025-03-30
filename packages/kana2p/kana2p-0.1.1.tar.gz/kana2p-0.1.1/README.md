# Japanese Katakana-Phonemes Conversion

## Installation

```bash
pip install kana2p
```

## Usage

```python
from kana2p import katakana2phonemes

# Convert Katakana to Phonemes
katakana = "ハロー、ワールデョ！"
phonemes = katakana2phonemes(katakana)
print(phonemes)
# Output: ["h", "a", "r", "o", ":", "、", "w", "a", ":", "r", "u", "dy", "o", "！"]
print(katakana2phonemes(katakana, normalize=True))
# Output: ["h", "a", "r", "o", ":", "w", "a", ":", "r", "u", "d", "y", "o"]
```

```python
from kana2p import phonemes2katakana

# Convert Phonemes to Katakana
phonemes = ["s", "i", ":", "kw", "a", ":", "s", "a", ":"]
katakana = phonemes2katakana(phonemes)
print(katakana)
# Output: "スィークァーサー"
```

## Note

### Special Characters
- The sokuon `ッ` is converted to the phoneme `q`.
- The prolonged sound mark `ー` is converted to the phoneme `:`.
- The syllabic nasal `ン` is converted to the phoneme `N`.
- `ヲ` is converted to `["o"]` rather than `["w", "o"]`.
- `ヶ` is converted to `["k", "a"]` rather than `["k", "e"]`.

### Rare Consonants
- Some rare consonants like `shw`, `dy`, `tsy`, `bw`, ... are included (e.g. `シュェ` -> `["shw", "e"]`, `デョ` -> `["dy", "o"]`).
- See `src/kana2p/const.py` for the full list of phoneme mappings.

### General Notes
- Only full-width Katakana are processed.
- If a character is not found in the mapping and normalize is False, the character is passed through unchanged.
- If normalize is True, characters not present in the mapping (e.g., non-Katakana characters) are excluded.
