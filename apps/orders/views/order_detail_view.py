from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import RoomOrder
from apps.orders.serializers.order_list import RoomOrderSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Room Orders'])
class RoomOrderDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = RoomOrder.objects.all()
    serializer_class = RoomOrderSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get('cancel', False):
            instance.is_canceled = True
            instance.save()
            return CustomResponse.success(
                message_key="CANCELED",
                data=None,
                status_code=status.HTTP_200_OK
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )