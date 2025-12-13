from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.reviews.models.hotel_reviews import HotelReview
from apps.reviews.models.room_reviews import RoomReview
from apps.reviews.serializers.reviews_detail import HotelReviewDetailSerializer, RoomReviewDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Reviews'])
class HotelReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = HotelReview.objects.all()
    serializer_class = HotelReviewDetailSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            data=serializer.data
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            data=serializer.data
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )


class RoomReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = RoomReview.objects.all()
    serializer_class = RoomReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS",
            data=serializer.data
        )

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            data=serializer.data
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            data=serializer.data
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )

