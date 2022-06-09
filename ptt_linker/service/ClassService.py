import asyncio
from os import stat
from tkinter.messagebox import NO
from requests_html import HTML, AsyncHTMLSession
from django.core.cache import cache
from ptt_linker.models.BoardClass import BoardNode, ClassNode


class ClassService:

    @staticmethod
    def _build_url(cls_num: int):
        return f'https://www.ptt.cc/cls/{cls_num}'

    @staticmethod
    async def _fetch_html(url) -> HTML:
        session = AsyncHTMLSession()
        response = await session.get(url, timeout=5)
        return response.html

    @staticmethod
    async def _fetch_class_task(cls_num: str) -> ClassNode:
        url = ClassService._build_url(cls_num)
        html: HTML = await ClassService._fetch_html(url)
        node = ClassNode.parse(cls_num, html)
        return node

    @staticmethod
    def fetch_class_boards(cls_number: int, recursive: bool) -> list[BoardNode]:

        if recursive:
            return asyncio.run(ClassService._fetch_boards(cls_number))
        else:
            return asyncio.run(ClassService._fetch_class_task(cls_number)).children_brd

    @staticmethod
    async def _fetch_boards(cls_number: int) -> list[BoardNode]:

        boards = cache.get(f'class:{cls_number}')
        if (not boards):
            boards = await ClassService._fetch_all_board_BFS(cls_number)
            cache.set(f'class:{cls_number}', boards, None)

        return boards

    @staticmethod
    async def _fetch_all_board_BFS(cls_number: int) -> list[BoardNode]:

        # Use BFS instead DFS to avoid maximum recursion depth issue.
        queue: list[int] = []
        boards: list[BoardNode] = []

        queue.append(cls_number)

        already_fetch_cls: set[int] = set()

        fetch_task = []

        first_run = True

        while fetch_task or first_run:
            first_run = False
            if (fetch_task):
                class_nodes: list[ClassNode] = await asyncio.gather(*fetch_task)
                for x in class_nodes:
                    queue += x.children_cls
                    boards += x.children_brd
            fetch_task.clear()
            while queue:
                current_cls = queue.pop(0)
                if (current_cls in already_fetch_cls):
                    continue

                already_fetch_cls.add(current_cls)
                fetch_task.append(
                    ClassService._fetch_class_task(int(current_cls)))

        return boards

    @staticmethod
    def fetch_hotboards() -> list[BoardNode]:

        url = 'https://www.ptt.cc/bbs/hotboards.html'
        html = asyncio.run(ClassService._fetch_html(url))
        node = ClassNode.parse(0, html)

        return node.children_brd
