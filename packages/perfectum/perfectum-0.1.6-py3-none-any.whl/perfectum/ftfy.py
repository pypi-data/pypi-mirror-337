from typing import Text
from .link import Link

try:
    import ftfy

    import_error = False
except ImportError:
    import_error = True


class Ftfy(Link):
    """
    Fixes text encoding issues and mojibake using ftfy library corrections.
    """

    def process(self, text: Text):
        if import_error:
            raise RuntimeError('requires "ftfy" feature enabled')

        return ftfy.fix_text(text, normalization=None)
