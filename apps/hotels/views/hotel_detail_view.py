from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelCreateSerializer
from apps.hotels.serializers.hotel_detail import HotelDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Hotels'])
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

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = HotelCreateSerializer(instance, data=request.data, context={"request": request}, partial=True)
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()
        response_serializer = HotelDetailSerializer(hotel, context={"request": request})
        return CustomResponse.success(
            message_key="UPDATED",
            data=response_serializer.data
        )