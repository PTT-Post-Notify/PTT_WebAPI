from certifi import contents
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, datetime
from ptt_linker.models import *
from ptt_linker.serializer import *

# Create your views here.


@api_view(['GET'])
def SearchData(request):
    return Response({'Data': 'HAHA'})


class ArticleView(APIView):

    def get(self, req, bid, aid):
        artical = Article(aid=aid, bid=bid, title='this is title',
                          comments=15, author='Chris', create_date=date.today())
        return Response(ArticleSerializer(artical).data)


@api_view(['GET'])
def get_board_articles(request, bid: str):
    artical = Article(aid='aid', bid=bid, title='this is title',
                      comments=15, author='Chris', create_date=date.today())
    board = Board(bid=bid, header='HAHA', articles=[artical])

    return Response(BoardSerializer(board).data)


@api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    comments = [Comment(author='User1', comment='Fuck', score=-1),
                Comment(author='User2', comment='推推', score=1)]

    article = ArticleDetail(aid=aid, bid=bid, title='this is title', content='WWWWW',
                            author='Chris', comments=comments, create_date=datetime.now())

    return Response(ArticleDetailSerializer(article).data)
