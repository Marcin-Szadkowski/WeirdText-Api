"""
Module to decode weird text.

"""
from abc import ABC, abstractmethod
from collections import defaultdict
from copy import copy
from typing import Any, List

from app.weird_text.parser import (DecodingException, ParserException, Token,
                                   WeirdTextParser)
from app.weird_text.utils import shuffle_possible, substitute_tokens


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
        """Partition words based on constructed key."""
        for token in self.tokens:
            dict_key = self._construct_key(token.value)

            self.partitions[dict_key].append(token)

    def get_matching_tokens(self, key: Any) -> List[Token]:
        return self.partitions.get(key)

    @abstractmethod
    def _construct_key(self, word: str) -> Any:
        """Construct hashable key. Implement some criteria for partitioning words."""

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

    """

    def __init__(self, tokens: List[Token]) -> None:
        super().__init__(tokens)

    def _construct_key(self, word: str) -> int:
        sub_word = word[1:-1]
        return self._sum_ascii(sub_word)

    def _sum_ascii(self, word: str) -> int:
        return sum(ord(letter) for letter in word)

    def is_deterministic(self, tokens: List[Token]) -> bool:
        """Last partition criteria should be deterministic."""
        return True


class Decoder:
    partition_classes = [InitialPartition, SetOfLettersPartition, ASCIISumPartition]

    @staticmethod
    def decode(text: str) -> str:
        result = []
        try:
            weird_text = WeirdTextParser(text)
        except ParserException as e:
            raise DecodingException(e)

        key_tokens, encoded_tokens = weird_text.key_tokens, weird_text.encoded_tokens
        encoded_tokens = list(filter(shuffle_possible, encoded_tokens))

        partition_classes = copy(Decoder.partition_classes)

        Decoder._partition_sets(key_tokens, encoded_tokens, partition_classes, result)
        print(result)
        return substitute_tokens(weird_text.encoded_text, result)

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
            encoded_token.coded = key_token.value
            result.append(encoded_token)
