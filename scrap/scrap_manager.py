from typing import Dict, Tuple, List, Optional

from bs4 import BeautifulSoup
import requests

from document.article import Article
from scrap.scrapper import Scrapper

class NoScrapper(ValueError):
    pass


class ScrapPagePredicate:
    def scraps_for(self, url: str, soup: BeautifulSoup):
        return False


class IncludesPredicate(ScrapPagePredicate):


    def __init__(self, includes):
        super().__init__()
        self.includes = includes

    def scraps_for(self, url: str, soup: BeautifulSoup):
        return self.includes in url


ScrapTuple = Tuple[ScrapPagePredicate, Scrapper]


class ScrapManager:
    scrapper: List[ScrapTuple] = []

    def register_includes_scrapper(self, includes: str, scrapper: Scrapper):
        self.register_scrapper(IncludesPredicate(includes), scrapper)

    def register_scrapper(self, predicate: ScrapPagePredicate, scrapper: Scrapper):
        self.scrapper.append((predicate, scrapper))

    def get_scrapper(self, url: str, soup: BeautifulSoup) -> Optional[Scrapper]:
        for scrap_tuple in self.scrapper:
            predicate = scrap_tuple[0]
            if predicate.scraps_for(url, soup):
                return scrap_tuple[1]
        return None

    def scrap(self, url: str, soup: BeautifulSoup) -> Article:
        scrapper = self.get_scrapper(url, soup)
        if scrapper is None:
            raise NoScrapper(url, soup)

        return scrapper.scrap(soup)

    def scrap_page(self, url) -> Optional[Article]:
        response = self.request_page(url)
        html_plain = response.text
        soup = BeautifulSoup(html_plain)

        scrapper = self.get_scrapper(url, soup)

        if not scrapper:
            return None

        return scrapper.scrap(soup)

    def request_page(self, url) -> requests.Response:
        return requests.get(url)


scrap_manager = ScrapManager()
