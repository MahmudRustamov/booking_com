from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from apps.reviews.models.hotel_reviews import HotelReview
from apps.reviews.models.room_reviews import RoomReview
from apps.reviews.serializers.reviews_detail import HotelReviewDetailSerializer, RoomReviewCreateSerializer
from apps.reviews.serializers.reviews_list import HotelReviewListSerializer, RoomReviewListSerializer
from apps.shared.utils.custom_response import CustomResponse


@extend_schema(tags=['Reviews'])
class HotelReviewListCreateApiView(ListCreateAPIView):
    queryset = HotelReview.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HotelReviewDetailSerializer
        return HotelReviewListSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.user)
        serializer.save(user=request.user if request.user.is_authenticated else None)
        return CustomResponse.success(
            message_key="CREATED",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


@extend_schema(tags=['Reviews'])
class RoomReviewListCreateApiView(ListCreateAPIView):

    def get_queryset(self):
        return RoomReview.objects.filter(
            room_id=self.kwargs['room_id']
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoomReviewCreateSerializer
        return RoomReviewListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        serializer.save(
            user=request.user if request.user.is_authenticated else None,
            room_id=self.kwargs['room_id']
        )

        return CustomResponse.success(
            message_key="CREATED",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )