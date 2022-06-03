from requests_html import Element


class Article:
    def __init__(self, bid: str, aid: str, title: str, comments_score: int,
                 author: str, create_date: str, link: str) -> None:
        self.Bid = bid
        self.Aid = aid
        self.Title = title
        self.Comments_Score = comments_score
        self.Author = author
        self.Create_date = create_date
        self.ArticleLink = link

    def __str__(self) -> str:
        return f"{self.bid}/{self.aid} : {self.title}"

    @classmethod
    def parse(cls, ele: Element):

        try:
            _score = ele.find('.nrec', first=True).text
            title = ele.find('.title', first=True).text
            score = int(_score) if _score.isnumeric() else 0
            author = ele.find('.author', first=True).text
            date = ele.find('.date', first=True).text
            articleLink = list(ele.find(
                '.title', first=True).absolute_links)[0]
            bid = articleLink.split('/')[-2]
            aid = articleLink.split('/')[-1][0:-5]  # remove .html
            article = cls(aid=aid, bid=bid, author=author, comments_score=score,
                          create_date=date, title=title, link=articleLink)

        except:
            return None

        return article
