from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.users.models.owners import Owners
from apps.users.serializers.owners import OwnerCreateSerializer, OwnerDetailSerializer, OwnerListSerializer
from apps.shared.permissions.mobile import IsMobileOrWebUser
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse


class OwnerListCreateApiView(ListCreateAPIView):
    serializer_class = OwnerCreateSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsMobileOrWebUser]

    def get_queryset(self):
        return Owners.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OwnerCreateSerializer

        if self.request.method == "GET" and self.request.device_type == "WEB":
            return OwnerListSerializer

        return OwnerDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            owner = serializer.save()
            response_serializer = OwnerDetailSerializer(owner, context={"request": request})

            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by("-id"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
                request=request
            )

        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )


class OwnerDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Owners.objects.all()
    serializer_class = OwnerDetailSerializer
    permission_classes = [IsMobileOrWebUser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OwnerDetailSerializer(instance, context={"request": request})

        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )
