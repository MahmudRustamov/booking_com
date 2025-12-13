from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from apps.rooms.models import Room
from apps.rooms.serializers.room_detail import RoomDetailSerializer
from apps.rooms.serializers.room_list import RoomCreateSerializer, RoomListSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse
import logging

logger = logging.getLogger(__name__)

@extend_schema(tags=['Rooms'])
class RoomListCreateApiView(ListCreateAPIView):
    serializer_class = RoomCreateSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Room.objects.filter(is_available=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoomCreateSerializer

        if self.request.method == "GET" and getattr(self.request, "device_type", None) == "WEB":
            return RoomListSerializer
        return RoomDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        response_serializer = RoomDetailSerializer(room, context={"request": request})
        return CustomResponse.success(
            message_key="CREATED",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by("-id"))
        page = self.paginate_queryset(queryset)
        serializer_class = self.get_serializer_class()
        if page is not None:
            serializer = serializer_class(page, many=True, context={"request": request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                request=request
            )

        serializer = serializer_class(queryset, many=True, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )
