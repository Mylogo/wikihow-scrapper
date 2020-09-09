from bs4 import BeautifulSoup

from document.article import Article


class Scrapper:
    def scrap(self, soup: BeautifulSoup) -> Article:
        raise NotImplemented()
