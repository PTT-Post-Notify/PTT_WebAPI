from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from ptt_linker.service import ClassService
from ptt_linker.serializer import BoardNodeSerializer


@api_view(['GET'])
def get_all_class(req: Request):

    data = ClassService.fetch_class_boards(1, True)
    result = BoardNodeSerializer(data, many=True).data
    return Response(result)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('recursive', openapi.IN_QUERY,
                      description="是否遞迴取得此分類底下的所有看板?", type=openapi.TYPE_BOOLEAN, default=True),
])
@api_view(['GET'])
def get_particular_class(req: Request, cls: int):

    _recu: str = req.query_params.get('recursive') or 'False'
    recu = True if _recu.lower() == "true" else False

    data = ClassService.fetch_class_boards(cls, recu)
    result = BoardNodeSerializer(data, many=True).data
    return Response(result)
