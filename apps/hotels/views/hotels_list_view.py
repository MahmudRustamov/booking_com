from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelCreateSerializer, HotelListSerializer
from apps.hotels.serializers.hotel_detail import HotelDetailSerializer
from apps.shared.permissions.mobile import IsMobileOrWebUser
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class HotelListCreateApiView(ListCreateAPIView):
    serializer_class = HotelCreateSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsMobileOrWebUser]

    def get_queryset(self):
        return HotelsModel.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HotelCreateSerializer
        elif self.request.method == "GET" and self.request.device_type == "WEB":
            return HotelListSerializer
        else:
            return HotelDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            response_serializer = HotelDetailSerializer(product, context={'request': request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        else:
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                errors=serializer.errors
            )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-id'))
        print(request.lang, request.device_type, "********")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                request=request
            )

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )