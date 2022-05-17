from typing import List

from parser import Token


def substitute_tokens(text: str, tokens: List[Token]) -> str:
    new = text
    for token in tokens:
        if token.encoded is None:
            continue
        new = new[: token.start] + token.encoded + new[token.end :]
    return new


def shuffle_possible(token: Token) -> bool:
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
