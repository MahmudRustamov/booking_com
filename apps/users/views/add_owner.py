from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.owners import Owners
from apps.users.serializers.add_user import HotelOwnerSerializer


class HotelOwnerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Owners.objects.all()
    serializer_class = HotelOwnerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hotel_owner = serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=HotelOwnerSerializer(hotel_owner).data,
                status_code=status.HTTP_201_CREATED
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )


class HotelOwnerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owners.objects.all()
    serializer_class = HotelOwnerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        serializer = self.get_serializer(hotel_owner, data=request.data, partial=True)
        if serializer.is_valid():
            hotel_owner = serializer.save()
            return CustomResponse.success(
                message_key="SUCCESS_MESSAGE",
                data=HotelOwnerSerializer(hotel_owner).data,
                status_code=status.HTTP_200_OK
            )
        return CustomResponse.error(
            message_key="VALIDATION_ERROR",
            errors=serializer.errors
        )

    def destroy(self, request, *args, **kwargs):
        hotel_owner = self.get_object()
        hotel_owner.delete()
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data={"id": kwargs.get("id")},
            status_code=status.HTTP_204_NO_CONTENT
        )
