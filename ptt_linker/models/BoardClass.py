from unittest import expectedFailure
from requests_html import HTML


class BoardNode:
    def __init__(self, parent_cls: int, name: str, title: str,
                 user_amount: int, link: str) -> None:

        self.parent_cls = parent_cls
        self.brd_name = name
        self.brd_title = title
        self.user_amount = user_amount
        self.link = link

    @classmethod
    def parse(cls, parent_class: int, html: HTML):
        name = html.find('.board-name', first=True).text
        title = html.find('.board-title', first=True).text
        amount_txt = html.find('.board-nuser', first=True).text
        user_amount = int(amount_txt) if amount_txt.isnumeric() else 0
        link = list(html.absolute_links)[0]

        instance = cls(parent_cls=parent_class,
                       name=name, title=title,
                       user_amount=user_amount, link=link)

        return instance


class ClassNode:
    def __init__(self, cls_number: int, children_cls: set[int], children_brd: list[BoardNode]) -> None:

        self.cls_number = cls_number
        self.children_cls = children_cls
        self.children_brd = children_brd

    @classmethod
    def parse(cls, cls_number: int, html: HTML):

        children = html.find('.b-ent')

        children_cls: set[int] = set()
        children_brd: list[BoardNode] = []

        for child in children:
            try:
                link: str = list(child.links)[0]  # eg. bbs/C_Chat
                is_board = link.startswith('/bbs')

                if is_board:
                    children_brd.append(BoardNode.parse(cls_number, child))
                else:  # eg. cls/15
                    children_cls.add(int(link.split('/')[-1]))
            except:
                continue

        instance = cls(cls_number=cls_number,
                       children_cls=children_cls,
                       children_brd=children_brd)

        return instance
