from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from typing import List


@dataclass
class Token:
    start: int
    end: int
    value: str
    coded: str = None


class DecodingException(Exception):
    """Base class for exceptions occuring on decode."""


class ParserException(DecodingException):
    """Exception while parsing input."""


class _Parser(ABC):
    tokenize_regex = re.compile(r"(\w+)", re.U)

    @abstractmethod
    def __init__(self, text: str) -> None:
        self.text = text

    def _tokenize_text(self, text: str = None) -> List[Token]:
        text = text or self.text
        return [
            Token(start=m.start(0), end=m.end(0), value=m[0])
            for m in self.tokenize_regex.finditer(text)
        ]


class PlainTextParser(_Parser):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self._tokens = self._tokenize_text()

    @property
    def tokens(self):
        return self._tokens


class WeirdTextParser(_Parser):
    separator = "\n-weird-\n"

    def __init__(self, text: str) -> None:
        super().__init__(text)
        encoded_text, key_words = self._parse()
        self._encoded_text = encoded_text
        self._key_tokens = self._tokenize_text(key_words)
        self._encoded_tokens = self._tokenize_text(encoded_text)

    @property
    def key_tokens(self):
        return self._key_tokens

    @property
    def encoded_tokens(self):
        return self._encoded_tokens

    @property
    def encoded_text(self):
        return self._encoded_text

    def _parse(self) -> tuple:
        if not self._is_valid_code_structure():
            raise ParserException(f"Inalid code structure. Should start with {repr(self.separator)}")
            
        code_elements = self._filter_empty(self._split_data())
        if len(code_elements) != 2:
            raise RuntimeError("Insufficient code elements.")
        return code_elements[0], code_elements[1]

    def _is_valid_code_structure(self) -> bool:
        return self.text.startswith(self.separator)

    def _split_data(self) -> list:
        data = self.text.split(self.separator)
        return data

    def _filter_empty(self, code_elements: list) -> tuple:
        return list(filter(lambda el: el, code_elements))
