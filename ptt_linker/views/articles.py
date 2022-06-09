from rest_framework.decorators import api_view
from rest_framework.response import Response
from ptt_linker.service import ArticleService
from ptt_linker.serializer import ArticleDetailSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='GET',
    operation_summary="取得特定文章",
    operation_description="由於文章 ID (eg: M.1654759600.A.D4C) 在不同的看板會有重複的情形, <br>\
                           因此必須提供看板 ID",
)
@api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    service = ArticleService()

    article = service.fetch_article_detail(bid, aid)

    return Response(ArticleDetailSerializer(article).data)
