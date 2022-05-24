from pydoc import describe
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
    openapi.Parameter('Desc', openapi.IN_QUERY,
                      description="是否倒序顯示", type=openapi.TYPE_BOOLEAN, default=True),
    openapi.Parameter('Skip', openapi.IN_QUERY,
                      description="欲 Skip 的文章數量", type=openapi.TYPE_INTEGER, default=0),
    openapi.Parameter('Take', openapi.IN_QUERY,
                      description="欲取回的文章數量", type=openapi.TYPE_INTEGER, default=20)
])
@api_view(['GET'])
def get_board_articles(req: Request, bid: str):
    _takeStr: str = req.query_params.get('Take') or "20"
    _skip: str = req.query_params.get('Skip') or "0"
    _desc: str = req.query_params.get('Desc') or 'True'

    _take = int(_takeStr) if _takeStr.isnumeric() else 201

    if (_take > 200 or _take < 0):
        return Response("Take limit is 200 records", status=400)

    b_service = BoardService()
    result = b_service.fetch_board_articles(
        bid=bid,
        title=None,
        author=None,
        score=None,
        take=_take,
        skip=int(_skip) if _skip else 0,
        desc=True if _desc.lower() == "true" else False
    )

    return Response(BoardSerializer(result).data)


@swagger_auto_schema(method='post', request_body=QueryParamsSerializer)
@api_view(['POST'])
def search_board_articles(req: Request, bid: str):
    body = req.data

    model_serializer = QueryParamsSerializer(data=body)
    model_serializer.is_valid(raise_exception=True)
    model = model_serializer.validated_data

    _take = model.get('Take')
    if (_take > 200 or _take < 0):
        return Response("Take limit is 200 records", status=400)

    b_service = BoardService()
    result = b_service.fetch_board_articles(
        bid=bid,
        title=model.get('Title'),
        author=model.get('Author'),
        score=model.get('Score'),
        take=_take,
        skip=model.get('Skip'),
        desc=True
    )
    return Response(BoardSerializer(result).data)


@ api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    comments = [Comment(author='User1', comment='Fuck', score=-1),
                Comment(author='User2', comment='推推', score=1)]

    article = ArticleDetail(aid=aid, bid=bid, title='this is title', content='WWWWW',
                            author='Chris', comments=comments, create_date=datetime.now())

    return Response(ArticleDetailSerializer(article).data)
