import copy
from dataclasses import dataclass, field
from email.policy import default
import random
import re
from typing import List, Optional, Tuple


@dataclass(kw_only=True)
class Token:
    start: int
    end: int
    value: str
    encoded: str = None


class WeirdText:
    text_format = "{separator}" "{text}" "{separator}" "{sorted_words}"
    separator = "\n-weird-\n"

    # @property
    # def separator(self) -> str:
    #     return "\n-weird-\n"

    def __init__(self, text: str, words: list) -> None:
        self.text = self.text_format.format(
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
    def encode(text: str):
        weird_text, sorted_words = Encoder._encode(text)

        return WeirdText(weird_text, sorted_words)

    @staticmethod
    def _encode(text: str) -> Tuple[str, list]:
        tokens = Encoder._tokenize_text(text)
        shuffled_words = []

        for token in tokens:
            if not Encoder._shuffle_possible(token):
                continue

            shuffled = Encoder._shuffle(token)
            shuffled_words.append(shuffled)

        text = Encoder._sub_tokens(text, tokens)
        return text, sorted(shuffled_words, key=str.lower)

    @staticmethod
    def _sub_tokens(text: str, tokens: list) -> str:
        new = text
        for token in tokens:
            if token.encoded is None:
                continue
            new = new[: token.start] + token.encoded + new[token.end :]
        return new

    @staticmethod
    def _tokenize_text(text: str) -> List[Token]:
        # TODO move it smwh else
        tokenize_re = re.compile(r"(\w+)", re.U)
        return [
            Token(m.start(0), m.end(0), m[0]) for m in tokenize_re.finditer(text)
        ]

    @staticmethod
    def _shuffle_possible(token: Token) -> bool:
        word = token.value
        if len(word) <= 3:
            return False

        sub = word[1:-1]
        letters = set()

        for letter in sub:
            letters.add(letter)
            if len(letters) == 2:
                return True

        return False

    @staticmethod
    def _shuffle(token: Token) -> str:
        word = copy.copy(token.value)
        original_sub, sub = word[1:-1], word[1:-1]

        while original_sub == sub:
            sub = "".join(random.sample(original_sub, len(original_sub)))

        token.encoded = word[0] + sub + word[-1]
        return token.value

    def _is_shuffled(word: str) -> bool:
        pass


if __name__ == "__main__":
    text = "This is a long looong test sentence,\nwith some big (biiiiig) words!"
    print(Encoder.encode(text))
