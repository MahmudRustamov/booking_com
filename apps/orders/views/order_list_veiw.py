from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema

from apps.orders.models import RoomOrder
from apps.orders.serializers.order_list import RoomOrderSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Room Orders'])
class RoomOrderListCreateApiView(ListCreateAPIView):
    serializer_class = RoomOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RoomOrder.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return CustomResponse.success(
            message_key="CREATED",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
