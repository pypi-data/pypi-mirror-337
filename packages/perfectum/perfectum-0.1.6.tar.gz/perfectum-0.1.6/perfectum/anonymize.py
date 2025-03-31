from .pattern_replace import PatternReplace
from .chain import Chain


DEFAULT_MAPPING = {
    "<email>": "<email>",
    "<phone>": "<phone>",
    "<snils>": "<snils>",
    "<passport>": "<passport>",
    "<inn>": "<inn>",
    "<ogrn>": "<ogrn>",
    "<vu>": "<vu>",
    "<card>": "<card>",
}


class Anonymize(Chain):
    """
    Collapses multiple consecutive spaces into a single space.

    # Output Masking

    - `<email>` -- Email address
    - `<phone>` -- Phone number
    - `<snils>` -- SNILS code
    - `<passport>` -- Passport code
    - `<inn>` -- INN code
    - `<ogrn>` -- Company registration number
    - `<vu>` -- Driver license
    - `<card>` -- Bank card code
    """

    def __init__(self, mapping: dict[str, str] = DEFAULT_MAPPING, level=0):
        self.mapping = mapping
        M = mapping
        chain = [
            PatternReplace(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", M["<email>"]
            ),
            PatternReplace(
                r"\+?(7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}",
                M["<phone>"],
            ),
            PatternReplace(r"\d{3}-\d{3}-\d{3}\s\d{2}", M["<snils>"]),
            PatternReplace(r"\b\d{2}\s?\d{2}\s?\d{6}\b", M["<passport>"]),
            PatternReplace(r"\b\d{10}\b|\b\d{12}\b", M["<inn>"]),
            PatternReplace(r"\b\d{13,15}\b", M["<ogrn>"]),
            PatternReplace(r"\b\d{2}[- ]?\d{2}[- ]?\d{6}\b", M["<vu>"]),
            PatternReplace(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", M["<card>"]),
        ]
        super().__init__(chain, level=0)

    def __repr__(self):
        return self._indentation + f"{type(self).__name__}"
