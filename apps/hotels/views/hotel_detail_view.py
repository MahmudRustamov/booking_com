from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelCreateSerializer
from apps.shared.utils.custom_response import CustomResponse


class HotelDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = HotelsModel.objects.all()
    serializer_class = HotelCreateSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            product = serializer.save()
            return CustomResponse.success(
                message_key="UPDATED_SUCCESSFULLY",
                data=self.get_serializer(product).data,
                status_code=status.HTTP_200_OK
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED_SUCCESSFULLY",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
