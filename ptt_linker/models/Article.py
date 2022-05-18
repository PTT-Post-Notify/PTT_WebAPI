from datetime import datetime


class Article:
    def __init__(self, bid: str, aid: str, title: str, comments_score: int, author: str, create_date: datetime) -> None:
        self.Bid = bid
        self.Aid = aid
        self.Title = title
        self.Comments_Score = comments_score
        self.Author = author
        self.Create_date = create_date

    def __str__(self) -> str:
        return f"{self.bid}/{self.aid} : {self.title}"
