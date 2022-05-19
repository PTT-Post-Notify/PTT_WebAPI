import re
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from datetime import date, datetime
from ptt_linker.models import *
from ptt_linker.serializer import *
from ptt_linker.service.BoardService import BoardService

# Create your views here.


@api_view(['GET'])
def SearchData(request):
    return Response({'Data': 'HAHA'})


class ArticleView(APIView):

    def get(self, req, bid, aid):
        artical = Article(aid=aid, bid=bid, title='this is title',
                          comments=15, author='Chris', create_date=date.today())
        return Response(ArticleSerializer(artical).data)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('Title', openapi.IN_QUERY,
                      description="文章標題", type=openapi.TYPE_STRING),
    openapi.Parameter('Desc', openapi.IN_QUERY,
                      description="是否倒序顯示", type=openapi.TYPE_BOOLEAN, default=True),
    openapi.Parameter('Skip', openapi.IN_QUERY,
                      description="欲 Skip 的文章數量", type=openapi.TYPE_INTEGER, default=0),
    openapi.Parameter('Take', openapi.IN_QUERY,
                      description="欲取回的文章數量", type=openapi.TYPE_INTEGER, default=20)
])
@api_view(['GET'])
def get_board_articles(req: Request, bid: str):
    take = req.query_params.get('take')
    b_service = BoardService()
    result = b_service.fetch_board_articles(
        bid, None, None, None, take, None, True)

    return Response(BoardSerializer(result).data)


@api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    comments = [Comment(author='User1', comment='Fuck', score=-1),
                Comment(author='User2', comment='推推', score=1)]

    article = ArticleDetail(aid=aid, bid=bid, title='this is title', content='WWWWW',
                            author='Chris', comments=comments, create_date=datetime.now())

    return Response(ArticleDetailSerializer(article).data)
