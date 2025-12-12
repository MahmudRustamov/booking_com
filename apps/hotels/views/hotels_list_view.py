from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelCreateSerializer, HotelListSerializer
from apps.hotels.serializers.hotel_detail import HotelDetailSerializer
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse
import logging

logger = logging.getLogger(__name__)


# class HotelListCreateApiView(ListCreateAPIView):
#     serializer_class = HotelCreateSerializer
#     pagination_class = CustomPageNumberPagination
#     # permission_classes = [IsHotelOwner]
#
#     def get_queryset(self):
#         return HotelsModel.objects.filter(is_active=True)
#
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return HotelCreateSerializer
#
#         if self.request.method == "GET" and getattr(self.request, "device_type", None) == "WEB":
#             return HotelListSerializer
#
#         return HotelDetailSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={"request": request})
#
#         try:
#             if serializer.is_valid(raise_exception=True):
#                 hotel = serializer.save()
#                 response_serializer = HotelDetailSerializer(hotel, context={"request": request})
#
#                 return CustomResponse.success(
#                     message_key="CREATED",
#                     data=response_serializer.data,
#                     status_code=status.HTTP_201_CREATED
#                 )
#
#         except Exception as e:
#             logger.exception("Failed to create hotel")
#             return CustomResponse.error(
#                 message_key="UNKNOWN_ERROR",
#                 errors={"detail": str(e)}
#             )
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset().order_by("-id"))
#         serializer_class = self.get_serializer_class()
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = serializer_class(page, many=True, context={"request": request})
#             return CustomResponse.success(
#                 message_key="SUCCESS_MESSAGE",
#                 data=serializer.data,
#                 status_code=status.HTTP_200_OK,
#                 request=request
#             )
#
#         serializer = serializer_class(queryset, many=True, context={"request": request})
#         return CustomResponse.success(
#             message_key="SUCCESS_MESSAGE",
#             data=serializer.data,
#             status_code=status.HTTP_200_OK,
#             request=request
#         )




class HotelListCreateApiView(ListCreateAPIView):
    serializer_class = HotelCreateSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return HotelsModel.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HotelCreateSerializer
        # Agar webdan GET bo‘lsa
        if self.request.method == "GET" and getattr(self.request, "device_type", None) == "WEB":
            return HotelListSerializer
        return HotelDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        hotel = serializer.save()
        response_serializer = HotelDetailSerializer(hotel, context={"request": request})
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