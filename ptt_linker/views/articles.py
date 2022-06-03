from rest_framework.decorators import api_view
from rest_framework.response import Response
from ptt_linker.service import ArticleService
from ptt_linker.serializer import ArticleDetailSerializer


@ api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    service = ArticleService()

    article = service.fetch_article_detail(bid, aid)

    return Response(ArticleDetailSerializer(article).data)
