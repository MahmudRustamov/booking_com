from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from .models import Room
from apps.rooms.serializers.room_list import RoomCreateSerializer
from apps.rooms.serializers.room_detail import RoomDetailSerializer
from ..shared.utils.custom_response import CustomResponse


class RoomListCreateApiView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            response_serializer = RoomDetailSerializer(room, context={'request': request})
            return CustomResponse.success(
                message_key="CREATED",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )


class RoomDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoomDetailSerializer(instance, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
