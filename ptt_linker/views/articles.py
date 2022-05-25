from rest_framework.decorators import api_view
from rest_framework.response import Response
from ptt_linker.models import *
from ptt_linker.serializer import *


@ api_view(['GET'])
def get_article_detail(req, bid: str, aid: str):

    comments = [Comment(author='User1', comment='Fuck', score=-1),
                Comment(author='User2', comment='推推', score=1)]

    article = ArticleDetail(aid=aid, bid=bid, title='this is title', content='WWWWW',
                            author='Chris', comments=comments, create_date=datetime.now())

    return Response(ArticleDetailSerializer(article).data)
