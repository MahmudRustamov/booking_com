from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.users.models.owners import Owners
from apps.users.models.user import User
from apps.users.serializers.owners import (
    OwnerCreateSerializer,
    OwnerDetailSerializer,
    OwnerListSerializer,
)
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.permissions.mobile import IsMobileOrWebUser
import logging

from apps.users.serializers.register import UserSerializer

logger = logging.getLogger(__name__)

class OwnerListCreateApiView(ListCreateAPIView):
    serializer_class = OwnerCreateSerializer
    pagination_class = CustomPageNumberPagination
    # permission_classes = [IsMobileOrWebUser]

    def get_queryset(self):
        return Owners.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OwnerCreateSerializer
        if self.request.method == "GET" and getattr(self.request, "device_type", None) == "WEB":
            return OwnerListSerializer
        return OwnerDetailSerializer


    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user_id = data.get("user")
        if not user_id:
            return CustomResponse.error(
                message_key="USER_REQUIRED",
                errors={"user": "User field is required"}
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return CustomResponse.error(
                message_key="USER_NOT_FOUND",
                errors={"user": "User with this id does not exist"}
            )

        if hasattr(user, "owners"):
            return CustomResponse.error(
                message_key="USER_ALREADY_OWNER",
                errors={"user": "This user is already linked to an owner"}
            )

        serializer = self.get_serializer(data={**data, "user": user.id}, context={"request": request})

        try:
            if serializer.is_valid(raise_exception=True):
                owner = serializer.save()
                response_serializer = OwnerDetailSerializer(owner, context={"request": request})
                return CustomResponse.success(
                    message_key="CREATED",
                    data=response_serializer.data,
                    status_code=status.HTTP_201_CREATED
                )
        except Exception as e:
            logger.exception("Failed to create owner")
            return CustomResponse.error(
                message_key="UNKNOWN_ERROR",
                errors={"detail": str(e)}
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



class ProfileRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    # GET method
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

    # PUT method
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key="UPDATED",
                data=serializer.data
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    # PATCH method
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message_key="UPDATED",
                data=serializer.data
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            data={}
        )



class OwnerDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Owners.objects.all()
    serializer_class = OwnerDetailSerializer
    # permission_classes = [IsMobileOrWebUser]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OwnerDetailSerializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )
