from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from ptt_linker.models import *
from ptt_linker.serializer import *
from ptt_linker.service import BoardService

# Create your views here.


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('Desc', openapi.IN_QUERY,
                          description="是否倒序顯示", type=openapi.TYPE_BOOLEAN, default=True),
        openapi.Parameter('Skip', openapi.IN_QUERY,
                          description="欲 Skip 的文章數量", type=openapi.TYPE_INTEGER, default=0),
        openapi.Parameter('Take', openapi.IN_QUERY, description="欲取回的文章數量",
                          type=openapi.TYPE_INTEGER, default=20)
    ],
    operation_summary="取得指定看板中的所有文章",
    operation_description="Take : 用來決定取得的文章數量，若留空則預設 20 最大為 200 <br>\
                           Skip : 用來跳過文章數量,在做 Paging 時會很有用",
)
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

    if (not result):
        return Response(f"Board Name : '{bid}' cannot be found")

    return Response(BoardSerializer(result).data)


@swagger_auto_schema(
    method='post',
    request_body=QueryParamsSerializer,
    operation_summary="在看板中搜尋指定條件的文章",
    operation_description="搜尋功能受限於 PTT Web 版的功能 <br>\
                           可指定以下三種條件 : <br>\
                           Title: 標題中包含的字詞<br>\
                           Author: 作者名稱包含的字詞<br>\
                           Score: 搜尋文章的 推/噓 文數量在指定數字以上(正數)或以下(負數)的文章. ",)
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

    if (not result):
        return Response(f"Board Name : '{bid}' cannot be found")

    return Response(BoardSerializer(result).data)
