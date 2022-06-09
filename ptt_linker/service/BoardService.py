from requests_html import HTMLSession, HTML
from ptt_linker.models import Board, Article


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
        article = Article.parse(item)
        if (article):
            articles.append(article)
    return articles


def _get_prev_page_index(html: HTML) -> int:
    btnGroup = html.find(
        '.btn-group-paging', first=True).find('.wide')
    prevlink: str = btnGroup[1].attrs.get('href')
    if (not prevlink):
        return None
    lastRoute = prevlink.split('/')[-1]
    if ('.html' in lastRoute):
        return int(lastRoute[5:-5])
    elif('search' in lastRoute):
        return int(lastRoute.split('&q')[0][12:])
    return None


class BoardService:

    def _fetch_html(self, url) -> HTML | None:
        session = HTMLSession()
        response = session.get(url)
        if (response.status_code != 200):
            return None
        return response.html

    def fetch_board_articles(self, bid: str, title: str, author: str, score: int,
                             take: int, skip: int, desc: bool) -> Board:

        if (title or author or score):
            return self.fetch_board_atticles_with_query_params(bid=bid, take=take, skip=skip, desc=desc,
                                                               title=title, author=author, score=score)
        else:
            return self.fetch_board_articles_without_query_params(bid=bid, take=take, skip=skip, desc=desc)

    def fetch_board_atticles_with_query_params(self, bid: str, title: str, author: str, score: int,
                                               take: int, skip: int, desc: bool) -> Board:

        page = 1
        articles = []

        url = _build_url(bid=bid, page=page,
                         title=title, author=author, score=score)

        html = self._fetch_html(url)
        if (not html):
            return None

        result = _parse_page_articles(html)

        articles += result

        if (articles):
            while (len(articles)-skip) < take:
                page = _get_prev_page_index(html)
                if (not page):
                    break
                url = _build_url(bid=bid, page=page,
                                 title=title, author=author, score=score)
                html = self._fetch_html(url)

                result = _parse_page_articles(html)

                articles += result

        board = Board(bid=bid, articles=articles[skip:take+skip], header=bid)

        return board

    def fetch_board_articles_without_query_params(self, bid: str,
                                                  take: int, skip: int,
                                                  desc: bool) -> Board:

        page = None
        if (not desc):
            page = 1

        articles = []

        url = _build_url(bid=bid, page=page)
        html = self._fetch_html(url)
        if (not html):
            return None

        result = _parse_page_articles(html)

        if (desc):
            result.reverse()
        articles += result

        while (len(articles)-skip) < take:
            if (not page):
                page = _get_prev_page_index(html)
                if (not page):
                    break
            elif (not desc):
                page += 1
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
