from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import List


@dataclass(kw_only=True)
class Token:
    start: int
    end: int
    value: str
    encoded: str = None


@dataclass(kw_only=True)
class EncodedToken(Token):
    decoded: str = None


class _Parser(ABC):
    token_class = Token

    @abstractmethod
    def __init__(self, text: str) -> None:
        self.text = text

    def _tokenize_text(self, text: str = None) -> List[Token]:
        text = text or self.text
        tokenize_re = re.compile(r"(\w+)", re.U)
        return [
            self.token_class(start=m.start(0), end=m.end(0), value=m[0])
            for m in tokenize_re.finditer(text)
        ]


class PlainTextParser(_Parser):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self._tokens = self._tokenize_text()

    @property
    def tokens(self):
        return self._tokens


class WeirdTextParser(_Parser):
    token_class = EncodedToken
    separator = "\n-weird-\n"

    def __init__(self, text: str) -> None:
        super().__init__(text)
        encoded_text, key_words = self._get_data()
        self._key_tokens = self._tokenize_text(key_words)
        self._encoded_tokens = self._tokenize_text(encoded_text)

    @property
    def key_tokens(self):
        return self._key_tokens

    @property
    def encoded_tokens(self):
        return self._encoded_tokens

    def _get_data(self) -> tuple:
        code_elements = self._filter_empty(self._split_data())
        if len(code_elements) != 2:
            raise RuntimeError("Insufficient code elements.")
        return code_elements[0], code_elements[1]

    def _split_data(self) -> list:
        data = self.text.split(self.separator)
        return data

    def _filter_empty(self, code_elements: list) -> tuple:
        return list(filter(lambda el: el, code_elements))
