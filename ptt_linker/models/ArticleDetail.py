from datetime import datetime
from requests_html import HTML
from itertools import takewhile


class Comment:
    def __init__(self, author: str, comment: str, score: int) -> None:
        self.Author = author
        self.Comment = comment
        self.Score = score

# =============== Article Detail ================


def _parse_atricle_comments(html: HTML) -> list[Comment]:

    def _parse_score(comment: HTML) -> int:
        meta = comment.find('.push-tag', first=True).text
        if meta == '推':
            return 1
        elif meta == '噓':
            return -1
        else:
            return 0

    def _parse_userId(comment: HTML) -> str:
        return comment.find('.push-userid', first=True).text

    def _parse_content(comment: HTML) -> str:
        return comment.find('.push-content', first=True).text[2:]

    comment_list = html.find('.push')

    comments = [Comment(_parse_userId(c), _parse_content(
        c), _parse_score(c)) for c in comment_list]

    return comments


def _parse_meta_data(html: HTML) -> dict[str, str]:

    meta_list = html.find('.article-metaline')

    meta: dict[str, str] = {}

    m: HTML
    for m in meta_list:
        tag = m.find('.article-meta-tag', first=True).text
        value = m.find(
            '.article-meta-value', first=True).text
        meta[tag] = value

    return meta


def _parse_main_content(html: HTML) -> str:

    main_content = html.find('#main-content', first=True).full_text

    content_list = main_content.split('\n')[1:]

    content_list = list(takewhile(
        lambda x: True if not x.startswith('※ 發信站') else False, content_list))

    content = str.join('\n', content_list)

    return content


class ArticleDetail:
    def __init__(self, bid: str, aid: str, title: str, content: str, comments: list[Comment],
                 author: str, create_date: datetime) -> None:
        self.Bid = bid
        self.Aid = aid
        self.Title = title
        self.Content = content
        self.Comments = comments
        self.Comments_Score = sum([x.Score for x in comments])
        self.Author = author
        self.Create_date = create_date

    @classmethod
    def parse(cls, bid: str, aid: str, html: HTML):

        meta = _parse_meta_data(html)
        main_content = _parse_main_content(html)
        comments = _parse_atricle_comments(html)

        obj = cls(bid=bid, aid=aid, author=meta['作者'],
                  title=meta['標題'], create_date=meta['時間'], content=main_content,
                  comments=comments)
        return obj
