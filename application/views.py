import json
from typing import Any

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest

from parsing.article_analysis import parse_article
from parsing.sentence_parser import parse_sentence
from scrap.scrap_manager import scrap_manager
from tagging.tagging import tag_tokens
from tokenization.tokenize import tokenize_text


def make_json_response(data: Any) -> HttpResponse:
    return HttpResponse(json.dumps(data))


def tokenize(request: HttpRequest) -> HttpResponse:
    text = request.GET.get('text')
    if not text:
        return HttpResponseBadRequest('No text')

    return make_json_response(tokenize_text(text))


def tag(request: HttpRequest) -> HttpResponse:
    text = request.GET.get('text')
    if not text:
        return HttpResponseBadRequest('No text')

    return make_json_response(tag_tokens(tokenize_text(text)))


def parse(request: HttpRequest) -> HttpResponse:
    text = request.GET.get('text')
    if not text:
        return HttpResponseBadRequest('No text')

    openie = request.GET.get('openie', 'false') == 'true'

    return make_json_response(parse_sentence(text, use_openie=openie).serialize())


def parse_wiki_how(request: HttpRequest) -> HttpResponse:
    text = request.GET.get('text')
    if not text:
        return HttpResponseBadRequest('No text')

    article = scrap_manager.scrap_page('https://www.wikihow.com/wikiHowTo?search=' + text)
    if article is None:
        return HttpResponseBadRequest('Please use another search term')

    openie = request.GET.get('openie', 'false') == 'true'

    return make_json_response(parse_article(article, use_openie=openie).serialize())


def test(request: HttpRequest) -> HttpResponse:
    return make_json_response('Henlo')
