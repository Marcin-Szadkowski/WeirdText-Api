from abc import ABC, abstractmethod
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from typing import Any, List
from parser import WeirdTextParser, Token, EncodedToken
from utils import shuffle_possible, substitute_tokens

# dokladne rozwiazanie nie zawsze istnieje

# wiemy jak wyglada kodowanie
"""
Dwa podjescia:
1. 
    1. dla kazdego kodowalnego slowa kodujemy je i sprawdzamy czy jest w slowniku - izi
    zlozonosc? duzo

2. 
    1. filtrujemy kodowalne slowa 
    2. dla kazdego slowa ze slownika 

optymalnie mozna najpierw przypasowac po:
a) dlugosci 

Mamy sety: 
"""


class Partition(ABC):
    @abstractmethod
    def __init__(self, tokens: List[Token]) -> None:
        super().__init__()
        self.tokens = tokens
        self.partitions = defaultdict(list)
        self._make_partition()

    def __iter__(self):
        return iter(self.partitions.items())

    def _make_partition(self) -> None:
        for token in self.tokens:
            dict_key = self._construct_key(token.value)

            self.partitions[dict_key].append(token)

    def get_matching_tokens(self, key: Any) -> List[Token]:
        return self.partitions.get(key)

    @abstractmethod
    def _construct_key(self, word: str) -> Any:
        """Construct hashable key."""

    @abstractmethod
    def is_deterministic(self, tokens: List[Token]) -> bool:
        """Check if words list has exact result."""


class InitialPartition(Partition):
    """
    Partition based on first & last letter and word length.

    """

    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def _construct_key(self, word: str) -> tuple:
        first, last = self._get_first_last_letter(word)
        word_length = len(word)

        return (first, last, word_length)

    def _get_first_last_letter(self, word: str) -> tuple:
        return word[0], word[-1]

    def is_deterministic(self, tokens: List[Token]) -> bool:
        return len(tokens) == 1


class SetOfLettersPartition(Partition):
    """
    Partition based on set of letters.

    """

    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def _construct_key(self, word: str) -> Any:
        sub_word = word[1:-1]
        return set(sub_word)

    def is_deterministic(self, tokens: List[Token]) -> bool:
        return len(tokens) == 1


class ASCIISumPartition(Partition):
    """
    Partition based on sum of ASCII codes.

    Note::
        Deterministic after previous partitions (?).

    """

    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def _construct_key(self, word: str) -> int:
        sub_word = word[1:-1]
        return self._sum_ascii(sub_word)

    def _sum_ascii(self, word: str) -> int:
        return sum(ord(letter) for letter in word)

    def is_deterministic(self, tokens: List[Token]) -> bool:
        return True


class Decoder:
    partition_classes = [InitialPartition, SetOfLettersPartition, ASCIISumPartition]

    @staticmethod
    def decode(text: str) -> str:
        result = []
        weird_text = WeirdTextParser(text)
        key_tokens, encoded_tokens = weird_text.key_tokens, weird_text.encoded_tokens
        encoded_tokens = list(filter(shuffle_possible, encoded_tokens))

        partition_classes = copy(Decoder.partition_classes)

        Decoder._partition_sets(key_tokens, encoded_tokens, partition_classes, result)
        return substitute_tokens(text, result)


    @staticmethod
    def _partition_sets(
        key_part: list, encoded_part: list, part_classes: list, result: List[Token]
    ):
        if len(part_classes) == 0:
            return

        _part_class = part_classes.pop(0)
        key_part = _part_class(key_part)
        encoded_part = _part_class(encoded_part)

        for key, tokens in key_part:
            matching_encoded_set = encoded_part.get_matching_tokens(key)

            if not key_part.is_deterministic(tokens):
                Decoder._partition_sets(
                    tokens, matching_encoded_set, copy(part_classes), result
                )
            else:
                Decoder._match_words_from(tokens, matching_encoded_set, result)

    @staticmethod
    def _match_words_from(key_tokens: list, encoded_tokens: list, result: list) -> None:
        if len(key_tokens) > 1:
            print("Warning: matching is not deterministic.")

        for key_token, encoded_token in zip(key_tokens, encoded_tokens):
            encoded_token.decoded = key_token.value
            result.append(encoded_token)


if __name__ == "__main__":
    text = (
        "\n-weird-\n"
        "Tihs is a lnog loonog tset sntceene,\n"
        "wtih smoe big (biiiiig) wdros!"
        "\n-weird-\n"
        "long looong sentence some test This with words"
    )
    print(Decoder.decode(text))
    # partition = InitialPartition(["word", "wrod", "marcin", "marian"])
    # for key, part in partition:
    #     print(key, part)
