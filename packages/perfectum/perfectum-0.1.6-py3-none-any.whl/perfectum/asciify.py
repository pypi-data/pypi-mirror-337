from typing import Text
import unicodedata
from .normalize_unicode import NormalizeUnicode
from .chain import Chain
from .replace import Replace

MINUS = "-"
DOUBLE_MINUS = 2 * MINUS

APOSTROPHE = "'"
QUOTE = '"'
ELLIPSIS = "..."

normalize = Chain(
    [
        # Hyphens
        Replace("\u002d", MINUS),
        Replace("\u00ad", MINUS),
        Replace("\u2010", MINUS),
        Replace("\u2011", MINUS),
        Replace("\u2012", MINUS),

        # En/Em dashes
        Replace("\u2013", MINUS),
        Replace("\u2014", DOUBLE_MINUS),
        Replace("\u2015", DOUBLE_MINUS),
        Replace("\u2e3a", DOUBLE_MINUS),
        Replace("\u2e3b", DOUBLE_MINUS),

        # Mathematical minus
        Replace("\u2212", MINUS),

        # Other
        Replace("\u058a", MINUS),
        Replace("\u1806", MINUS),

        # Single quotes
        Replace("\u2018", APOSTROPHE),
        Replace("\u2019", APOSTROPHE),
        Replace("\u201a", APOSTROPHE),
        Replace("\u201b", APOSTROPHE),

        # Double quotes
        Replace("\u201c", QUOTE),
        Replace("\u201d", QUOTE),
        Replace("\u201e", QUOTE),
        Replace("\u201f", QUOTE),

        # Angle quotes
        Replace("\u00ab", QUOTE),
        Replace("\u00bb", QUOTE),
        Replace("\u2039", QUOTE),
        Replace("\u203a", QUOTE),

        # Prime quotes
        Replace("\u2032", APOSTROPHE),
        Replace("\u2033", QUOTE),
        Replace("\u2035", APOSTROPHE),
        Replace("\u2036", QUOTE),

        # CJK quotes
        Replace("\u300c", QUOTE),
        Replace("\u300d", QUOTE),
        Replace("\u301d", QUOTE),
        Replace("\u301e", QUOTE),

        # Ellipsis
        Replace("\u2026", ELLIPSIS),
        Replace("\u22ef", ELLIPSIS),
        Replace("\u00b7", MINUS),

        # Fractions
        Replace("\u00bc", "1/4"),
        Replace("\u00bd", "1/2"),
        Replace("\u00be", "3/4"),

        # Arrows
        Replace("\u2192", "->"),
        Replace("\u2190", "<-"),
        Replace("\u2194", "<->"),
    ]
)

class Asciify(NormalizeUnicode):
    """
    Converts Unicode text to ASCII by removing diacritics and non-ASCII characters.
    """

    def __init__(self, level=0):
        super().__init__("NFKD", level)

    def process(self, text: Text):
        text = super().process(text)
        text = normalize(text)
        text = "".join(
            [
                character
                for character in text
                if not unicodedata.combining(character)
            ]
        )
        return text

    def __repr__(self):
        return self._indentation + type(self).__name__
