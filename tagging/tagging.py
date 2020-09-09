from typing import Tuple

import nltk

from tokenization.tokenize import Tokens

Word = str
WordType = str
Tag = Tuple[Word, WordType]


def tag_tokens(tokens: Tokens) -> Tag:
    return nltk.pos_tag(tokens)
