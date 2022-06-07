from unittest import result
from requests_html import HTML, HTMLSession

from ptt_linker.models.BoardClass import BoardNode, ClassNode


class ClassService:

    @staticmethod
    def _build_url(cls_num: int):
        return f'https://www.ptt.cc/cls/{cls_num}'

    @staticmethod
    def _fetch_html(url) -> HTML:
        session = HTMLSession()
        response = session.get(url, timeout=5)
        return response.html

    @staticmethod
    def fetch_class_boards(cls_number: int, recursive: bool) -> list[BoardNode]:
        if recursive:
            return ClassService._fetch_all_board_BFS(cls_number)
        else:
            return ClassService._fetch_boards(cls_number)

    @staticmethod
    def _fetch_boards(cls_number: int) -> list[BoardNode]:

        url = ClassService._build_url(cls_number)
        html: HTML = ClassService._fetch_html(url)
        node = ClassNode.parse(html)

        return node.children_brd

    @staticmethod
    def _fetch_all_board_BFS(cls_number: int) -> list[BoardNode]:

        # Use BFS instead DFS to avoid maximum recursion depth issue.
        queue: list[int] = []
        boards: list[BoardNode] = []
        queue.append(cls_number)

        already_fetch_cls: set[int] = set()

        while queue:
            current_cls = queue.pop(0)
            if (current_cls in already_fetch_cls):
                continue

            already_fetch_cls.add(current_cls)

            url = ClassService._build_url(current_cls)
            html: HTML = ClassService._fetch_html(url)
            node = ClassNode.parse(html)
            queue += node.children_cls
            boards += node.children_brd

        return boards
