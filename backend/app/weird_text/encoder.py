import copy
from dataclasses import dataclass, field
import random
from typing import Tuple

from app.weird_text.parser import PlainTextParser, Token
from app.weird_text.utils import shuffle_possible, substitute_tokens


class WeirdText:
    encoding_format = "{separator}" "{text}" "{separator}" "{sorted_words}"
    separator = "\n-weird-\n"

    def __init__(self, text: str, words: list) -> None:
        self.text = self.encoding_format.format(
            separator=self.separator, text=text, sorted_words=" ".join(words)
        )

    def __str__(self) -> str:
        return self.text


# TODO probably all static methods
class Encoder:
    """
    foreach word in words:
        shuffle(w[..o.r..]d) # if possible shuffle(word) != word
        if is_shuffled(word):
            shuffled_words += word

    sorted(shuffled_words)
    """

    @staticmethod
    def encode(text: str) -> WeirdText:
        tokens = PlainTextParser(text).tokens
        shuffled_tokens, sorted_words = Encoder._encode(tokens)
        weird_text = substitute_tokens(text, shuffled_tokens)

        return str(WeirdText(weird_text, sorted_words))

    @staticmethod
    def _encode(tokens: list) -> Tuple[list, list]:
        shuffled_tokens = []
        words = []

        for token in tokens:
            if not shuffle_possible(token):
                continue

            shuffled = Encoder._shuffle_word(token)
            shuffled_tokens.append(token)
            words.append(shuffled)

        return shuffled_tokens, sorted(words, key=str.lower)

    @staticmethod
    def _shuffle_word(token: Token) -> str:
        word = copy.copy(token.value)
        original_sub, sub = word[1:-1], word[1:-1]

        while original_sub == sub:
            sub = "".join(random.sample(original_sub, len(original_sub)))

        token.coded = word[0] + sub + word[-1]
        return token.value
