
from requests_html import HTMLSession, Element, HTML
from ptt_linker.models import ArticleDetail, Comment
from itertools import takewhile
from datetime import datetime


def _url_builder(bid: str, aid: str):
    url = f'https://www.ptt.cc/bbs/{bid}/{aid}.html'
    return url


class ArticleService():

    def _fetch_html(self, url) -> HTML | None:
        session = HTMLSession()
        response = session.get(url)
        if (response.status_code != 200):
            return None
        return response.html

    def fetch_article_detail(self, bid: str, aid: str) -> ArticleDetail | None:

        url = _url_builder(bid, aid)
        html = self._fetch_html(url)

        if (not html):
            return None
        article = ArticleDetail.parse(bid, aid, html)

        return article
