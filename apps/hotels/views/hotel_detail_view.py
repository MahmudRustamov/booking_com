from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelCreateSerializer
from apps.hotels.serializers.hotel_detail import HotelDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


# class HotelDetailApiView(RetrieveUpdateDestroyAPIView):
#     queryset = HotelsModel.objects.all()
#     serializer_class = HotelDetailSerializer
#     # permission_classes = [IsHotelOwner]
#
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = HotelDetailSerializer(instance, context={"request": request})
#
#         return CustomResponse.success(
#             message_key="SUCCESS_MESSAGE",
#             data=serializer.data
#         )
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#
#         if serializer.is_valid():
#             hotel = serializer.save()
#             return CustomResponse.success(
#                 message_key="UPDATED",
#                 data=self.get_serializer(hotel).data,
#                 status_code=status.HTTP_200_OK
#             )
#
#         return CustomResponse.error(
#             message_key="VALIDATION_ERROR",
#             errors=serializer.errors
#         )
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#
#         return CustomResponse.success(
#             message_key="DELETED",
#             data=None,
#             status_code=status.HTTP_204_NO_CONTENT
#         )



class HotelDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = HotelsModel.objects.all()
    serializer_class = HotelDetailSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = HotelDetailSerializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = HotelCreateSerializer(instance, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()
        response_serializer = HotelDetailSerializer(hotel, context={"request": request})
        return CustomResponse.success(
            message_key="UPDATED",
            data=response_serializer.data
        )