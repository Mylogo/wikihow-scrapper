from typing import List

from document.article import Article
from parsing.sentence_parser import parse_sentence
from parsing.text_analysis import TextAnalysis


class ArticleAnalysis:
    def __init__(self, article, use_openie=False):
        self.article = article
        self.use_openie = use_openie
        self.analyzed_sections: List[TextAnalysis] = []
        self.__analyze_article()

    def __analyze_article(self):
        for section in self.article.sections:
            section_text_analysis = parse_sentence(section.text, use_openie=self.use_openie)
            self.analyzed_sections.append(section_text_analysis)

    def serialize(self):
        data = {
            "article": self.article.serialize(),
            "sections": list(map(lambda text_analysis: text_analysis.serialize(), self.analyzed_sections))
        }
        return data


def parse_article(article: Article, use_openie=False) -> ArticleAnalysis:
    return ArticleAnalysis(article, use_openie=use_openie)
