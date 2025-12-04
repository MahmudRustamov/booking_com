from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from apps.shared.utils.custom_pagination import CustomPageNumberPagination
from apps.users.models.owners import Owners
from apps.users.models.user import User
from apps.users.serializers.owners import OwnersCreateSerializer, OwnersDetailSerializer
from apps.shared.utils.custom_response import CustomResponse


class OwnersListCreateApiView(ListCreateAPIView):
    queryset = Owners.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = OwnersCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user_id = data.get('user')
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                data['user'] = user.id
            except User.DoesNotExist:
                return CustomResponse.error(
                    message_key="USER_NOT_FOUND",
                    errors={"user": "User with this id does not exist"}
                )
        else:
            return CustomResponse.error(
                message_key="USER_REQUIRED",
                errors={"user": "User field is required"}
            )

        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            owner = serializer.save()
            response_serializer = OwnersDetailSerializer(owner, context={'request': request})
            return CustomResponse.success(
                message_key="OWNER_CREATED",
                data=response_serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('company_name')
        serializer = OwnersDetailSerializer(queryset, many=True, context={'request': request})
        return CustomResponse.success(
            message_key="ORGANIZER_LIST",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            request=request
        )


class OwnersDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Owners.objects.all()
    serializer_class = OwnersDetailSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="ORGANIZER_DETAIL",
            data=serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            organizer = serializer.save()
            return CustomResponse.success(
                message_key="ORGANIZER_UPDATED",
                data=self.get_serializer(organizer).data,
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
            message_key="ORGANIZER_DELETED",
            data=None,
            status_code=status.HTTP_204_NO_CONTENT
        )
