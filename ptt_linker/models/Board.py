from .Article import Article


class Board:
    def __init__(self, bid: str, header: str, articles: list[Article]) -> None:
        self.Bid = bid
        self.Header = header
        self.Articles = articles
        pass
