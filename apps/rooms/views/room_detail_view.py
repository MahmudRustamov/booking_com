# views.py
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.rooms.models import Room
from apps.rooms.serializers.room_list import RoomCreateSerializer, RoomListSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Rooms'])
class RoomDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoomListSerializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoomCreateSerializer(instance, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        response_serializer = RoomListSerializer(room, context={"request": request})
        return CustomResponse.success(
            message_key="UPDATED",
            data=response_serializer.data
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoomCreateSerializer(
            instance, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        room = serializer.save()
        response_serializer = RoomListSerializer(room, context={"request": request})
        return CustomResponse.success(
            message_key="UPDATED",
            data=response_serializer.data
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            data=None
        )
