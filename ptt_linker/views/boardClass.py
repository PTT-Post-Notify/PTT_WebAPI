from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ptt_linker.service import ClassService
from ptt_linker.serializer import BoardNodeSerializer


@swagger_auto_schema(
    method='GET',
    operation_summary="取得 PTT 的所有看板資料",
    operation_description="Note!! : 此功能會由 PTT 的 主分類 (Root Class:1) 使用 BFS 的方式訪問所有看板<br>\
                           目前的看板數量約有 13k 左右，Swagger 無法接下如此大量的 Json 內容<br> \
                           若要測試，請另外使用 PostMan 等工具"
)
@api_view(['GET'])
def get_all_class(req: Request):

    data = ClassService.fetch_class_boards(1, True)
    result = BoardNodeSerializer(data, many=True).data
    return Response(result)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('recursive', openapi.IN_QUERY,
                          description="是否遞迴取得此分類底下的所有看板?", type=openapi.TYPE_BOOLEAN, default=True),
    ],
    operation_summary="取得特定分類底下的看板",
    operation_description="Note!! : 若 recursive 的條件為 True，則 Swagger 未必有能力收下結果")
@api_view(['GET'])
def get_particular_class(req: Request, cls: int):

    _recu: str = req.query_params.get('recursive') or 'False'
    recu = True if _recu.lower() == "true" else False

    data = ClassService.fetch_class_boards(cls, recu)
    result = BoardNodeSerializer(data, many=True).data
    return Response(result)


@swagger_auto_schema(
    method='get',
    operation_summary='取得熱門看板',
    operation_description='https://www.ptt.cc/bbs/hotboards.html'
)
@api_view(['GET'])
def get_hotboards(req: Request):

    hotBoards = ClassService.fetch_hotboards()
    result = BoardNodeSerializer(hotBoards, many=True).data
    return Response(result)
