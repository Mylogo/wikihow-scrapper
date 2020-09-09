from typing import List, Dict, Optional
import json

from nltk.corpus.reader import Synset
from spacy.tokens import Doc, Span, Token
from nltk.corpus import wordnet
from nltk.wsd import lesk
from pyopenie import OpenIE5

extractor = OpenIE5('http://localhost:8000')


def serialize_synset(synset: Synset, serialize_additional_data=False) -> Dict[str, any]:
    data = {
        "name": synset.name(),
        "definition": synset.definition(),
    }

    if serialize_additional_data:
        synonyms = []
        antonyms = []
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
            for antonym in lemma.antonyms():
                antonyms.append(antonym.name())
        data["synonyms"] = synonyms
        data["antonyms"] = antonyms
        data["hyponyms"] = list(map(lambda synset: synset.name(), synset.hyponyms()))

    return data


def _token_pos_to_nltk_pos(token: Token) -> Optional[str]:
    spacy_pos = token.pos_
    if not spacy_pos:
        return None

    return spacy_pos[0].lower()


class WordAnalysis:
    def __init__(self, token: Token):
        self.token = token
        self.synsets = wordnet.synsets(token.text)
        self.probable_synset = None

    def calculate_probable_synset(self, sentence: List[str]):
        if self.probable_synset:
            return

        self.probable_synset = lesk(sentence, self.token.text, pos=_token_pos_to_nltk_pos(self.token))

    def serialize(self, serialize_all_synsets=True) -> Dict[str, any]:
        data = {
            "token_id": self.token.i,
        }

        if serialize_all_synsets:
            data["synsets"] = list(map(serialize_synset, self.synsets))

        if self.probable_synset:
            data['probable_synset'] = serialize_synset(self.probable_synset, True)

        return data


class SentenceAnalysis:
    def __init__(self, sentence: Span):
        self.sentence = sentence
        self.openie = None
        # self.__extract_openie_triples()

    def __extract_openie_triples(self):
        self.openie = extractor.extract(self.sentence.text)

    def serialize(self):
        return {
            "sentence": self.sentence.text,
            # "openie": self.openie
        }


class TextAnalysis:
    def __init__(self, doc: Doc, use_openie=False):
        self.doc = doc
        self.words: List[WordAnalysis] = []
        self.sentences: List[SentenceAnalysis] = []

        if use_openie:
            self.openie = extractor.extract(doc.text)
        else:
            self.openie = None

        self.__populate_words()
        # self.__populate_sentences()

    def __populate_words(self):
        for token in self.doc:
            word_analysis = WordAnalysis(token)
            word_analysis.calculate_probable_synset(token.sent.text.split(' '))
            self.words.append(word_analysis)

    def __populate_sentences(self):
        for sentence in self.doc.sents:
            sentence_analysis = SentenceAnalysis(sentence)
            self.sentences.append(sentence_analysis)

    def serialize(self) -> Dict[str, any]:
        data = {
            "doc": serialize_doc(self.doc),
            # "sentences": list(map(lambda sentence: sentence.serialize(), self.sentences))
        }

        words = {}
        for word in self.words:
            words[word.token.i] = word.serialize()

        data["words"] = words

        if self.openie:
            data["openie"] = self.openie

        return data


def serialize_doc(doc: Doc) -> Dict[str, any]:
    dep = []
    return {
        'text': doc.text,
        'tokens': list(map(serialize_token, doc.__iter__())),
        'noun_chunks': list(map(serialize_span, doc.noun_chunks)),
        'data': doc.to_json(),
        # 'dep': dep,
    }


def serialize_span(span: Span) -> Dict[str, any]:
    return {
        'text': span.text,
        'type': span.label_,
    }


def serialize_token(token: Token, deep=True) -> Dict[str, any]:
    doc = token.doc
    token_data = {"text": token.text, "id": token.i, "start": token.idx, "end": token.idx + len(token)}
    if doc.is_tagged:
        token_data["pos"] = token.pos_
        token_data["tag"] = token.tag_
    if doc.is_parsed:
        token_data["dep"] = token.dep_
        # Maybe this is important, it returns a token tho.
        if token.head and deep:
            token_data["head"] = token.head.i
        #     token_data["head"] = serialize_token(token.head, deep=False)
    return token_data
