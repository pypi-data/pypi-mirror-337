from typing import Text, Optional
from .link import Link

try:
    from navec import Navec
    from slovnet import NER

    import_error = False
except ImportError:
    import_error = True

DEFAULT_MAPPING = {
    "PER": "<person>",
    "LOC": "<location>",
    "ORG": "<organization>",
}


class Ner(Link):
    """
    Replaces named entities with specified tags using NLP.
    """

    def __init__(
        self,
        navec_path: str,
        ner_path: str,
        mapping: dict[str, str] = DEFAULT_MAPPING,
        level=0,
    ):
        super().__init__(level)
        self.navec_path = navec_path
        self.ner_path = ner_path
        self.mapping = mapping

        if import_error:
            raise RuntimeError('requires "ner" feature enabled')

        try:
            self.navec = Navec.load(navec_path)
        except ValueError:
            raise RuntimeError(
                "download navec model from repository: https://github.com/natasha/navec#downloads"
            )

        try:
            self.ner = NER.load(ner_path)
        except ValueError:
            raise RuntimeError(
                "download slovnet model from repository: https://github.com/natasha/slovnet#downloads"
            )

        self.ner.navec(self.navec)

    def process(self, text: Text):
        ner = self.ner(text)
        for span in ner.spans:
            if span.type in self.mapping:
                span_text = ner.text[span.start : span.stop]
                text = text.replace(span_text, self.mapping[span.type])
        return text

    def __repr__(self):
        return self._indentation + f'{type(self).__name__}("{self.model_name}")'
