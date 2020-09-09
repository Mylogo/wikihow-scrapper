import requests
from bs4 import BeautifulSoup

from document.article import Article
from document.section import Section
from scrap.scrapper import Scrapper


def _scrap_section(soup: BeautifulSoup) -> Section:
    for unneeded in soup(['script', 'style', 'sup']):
        unneeded.decompose()

    # Some unnecessary meta data that would be printed out
    image = soup.select_one('div.image_details')
    if image:
        image.decompose()

    return Section(soup.get_text(strip=True))


def _scrap_article(soup: BeautifulSoup) -> Article:
    title_tag = soup.select_one('h1.title_md')
    if title_tag is None:
        title_tag = soup.select_one('h1.title_lg')
    if title_tag is None:
        title_tag = soup.select_one('h1.title_sm')
    title = title_tag.text
    article = Article(title)

    # step_div = soup.select_one('div#steps ol')
    step_div = soup.select_one('div ol')
    for child in step_div.findChildren('li', recursive=False):
        try:
            div = child.select_one('div.step')
            article.append_section(_scrap_section(div))
        except Exception as e:
            print("Error parsing section:", e)

    return article


class HowtoScrapper(Scrapper):
    def scrap(self, soup: BeautifulSoup) -> Article:
        possible_articles = soup.select('a.result_link')
        best_article = None

        for article in possible_articles:
            print("ARTICLE:", article.get_text())
            if 'Category' in article.get_text():
                continue
            best_article = article
            break

        if best_article is None:
            raise ValueError('No best article for this search')

        href = best_article.get('href')
        if href is None:
            raise ValueError('Best article does not have an href')

        wikihow_article = requests.get(href)
        article_text = wikihow_article.text
        soup = BeautifulSoup(article_text)

        return _scrap_article(soup)
