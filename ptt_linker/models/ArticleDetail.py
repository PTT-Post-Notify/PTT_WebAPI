from datetime import datetime


class Comment:
    def __init__(self, author: str, comment: str, score: int) -> None:
        self.Author = author
        self.Comment = comment
        self.Score = score


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
