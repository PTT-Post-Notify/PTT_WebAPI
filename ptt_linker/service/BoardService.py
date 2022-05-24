from requests_html import HTMLSession, Element, HTML
from ptt_linker.models import Board
from ptt_linker.models.Article import Article


def create_article(input: Element) -> Article:

    try:
        _score = input.find('.nrec', first=True).text
        title = input.find('.title', first=True).text
        score = int(_score) if _score.isnumeric() else 0
        author = input.find('.author', first=True).text
        date = input.find('.date', first=True).text
        articleLink = list(input.find('.title', first=True).absolute_links)[0]
        bid = articleLink.split('/')[-2]
        aid = articleLink.split('/')[-1][0:-5]  # remove .html
        article = Article(aid=aid, bid=bid, author=author, comments_score=score,
                          create_date=date, title=title, link=articleLink)

    except:
        return None

    return article


def _build_url(bid: str, page: int,
               title: str = None, author: str = None, score: int = None) -> str:

    url = f'https://www.ptt.cc/bbs/{bid}/'
    searchParams = []
    if (title):
        searchParams.append(title)
    if (author):
        searchParams.append(f'author%3A{author}')
    if(score):
        searchParams.append(f'recommend%3A{score}')

    if (len(searchParams)):
        url += f'search?page={page or 1}&q={"+".join(searchParams)}'
    else:
        url += f'index{page or ""}.html'

    return url


def _parse_page_articles(html: HTML) -> list[Article]:
    articles = []
    for item in html.find('.bbs-screen > div'):
        if 'search-bar' in item.attrs['class']:
            continue
        if 'r-list-sep' in item.attrs['class']:  # 代表後續的文章為至底文章
            break
        article = create_article(item)
        if (article):
            articles.append(article)
    return articles


def _get_prev_page_index(html: HTML):
    btnGroup = html.find(
        '.btn-group-paging', first=True).find('.wide')
    prevlink: str = btnGroup[1].attrs.get('href')
    lastRoute = prevlink.split('/')[-1]
    if ('.html' in lastRoute):
        return lastRoute[5:-5]
    return None


class BoardService:

    def _fetch_html(self, url) -> HTML:
        session = HTMLSession()
        response = session.get(url)
        return response.html

    def fetch_board_articles(self, bid: str, title: str, author: str, score: int,
                             take: int, skip: int, desc: bool) -> Board:

        return self.fetch_board_articles_without_query_params(bid=bid, take=take, skip=skip, desc=desc)

        page = None
        if (title or author or score):
            page = 1
        articles = []

        url = _build_url(bid=bid, title=title, author=author,
                         score=score, page=page)
        html = self._fetch_html(url)

        result = _parse_page_articles(html)

        if (desc):
            result.reverse()
        articles += result

        while len(articles) < take:
            if (not page):
                page = _get_prev_page_index(html)
            elif (title or author or score):
                page += 1
            else:
                page -= 1

            url = _build_url(bid=bid, title=title, author=author,
                             score=score, page=page)
            html = self._fetch_html(url)

            result = _parse_page_articles(html)

            if(desc):
                result.reverse()
            articles = articles + result

        board = Board(bid=bid, articles=articles[0:take], header=bid)

        return board

    def fetch_board_atticles_with_query_params(self, bid: str, title: str, author: str, score: int,
                                               take: int, skip: int, desc: bool) -> Board:

        pass

    def fetch_board_articles_without_query_params(self, bid: str,
                                                  take: int, skip: int,
                                                  desc: bool) -> Board:

        page = None
        if (not desc):
            page = 1

        articles = []

        url = _build_url(bid=bid, page=page)
        html = self._fetch_html(url)

        result = _parse_page_articles(html)

        if (desc):
            result.reverse()
        articles += result

        while (len(articles)-skip) < take:
            if (not page):
                page = _get_prev_page_index(html)
            else:
                page -= 1

            url = _build_url(bid=bid, page=page)
            html = self._fetch_html(url)

            result = _parse_page_articles(html)

            if(desc):
                result.reverse()
            articles += result

        board = Board(bid=bid, articles=articles[skip:take+skip], header=bid)

        return board
