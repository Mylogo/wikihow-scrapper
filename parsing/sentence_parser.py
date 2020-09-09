
import spacy

from parsing.text_analysis import TextAnalysis

nlp = spacy.load('en_core_web_sm')


def parse_sentence(sentence: str, use_openie=False) -> TextAnalysis:
    doc = nlp(sentence)
    return TextAnalysis(doc, use_openie=use_openie)
