from typing import Text
from .link import Link
import unicodedata


class RemovePunctuation(Link):
    """
    Removes all punctuation characters.
    """

    def is_punctuation(self, character: str):
        category = unicodedata.category(character)
        return category.startswith("P")

    def process(self, text: Text):
        return "".join(
            [character for character in text if not self.is_punctuation(character)]
        )
