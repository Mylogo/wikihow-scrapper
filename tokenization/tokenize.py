from typing import List

import nltk

Tokens = List[str]


def tokenize_text(text: str) -> Tokens:
    return nltk.word_tokenize(text)
