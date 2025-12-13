from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.shared.utils.custom_response import CustomResponse
from apps.users.models.user import VerificationCode, User
from apps.users.serializers.register import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.exceptions import TokenError

@extend_schema(tags=['Auth'])
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'Verification code sent to email'}, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Auth'])
class VerifyEmailAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    @staticmethod
    def post(request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

        try:
            verification = VerificationCode.objects.filter(user=user, code=code, used=False).latest('created_at')
        except VerificationCode.DoesNotExist:
            return Response({'error': 'Invalid or expired code'}, status=400)

        if not verification.is_valid():
            return Response({'error': 'Code expired'}, status=400)

        user.is_active = True
        user.save()
        verification.used = True
        verification.save()

        return Response({'detail': 'Email verified successfully.'})


@extend_schema(tags=['Auth'])
class VerifyLoginAPIView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "detail": "Login successful"
        }, status=status.HTTP_200_OK)




@extend_schema(tags=['Auth'])
class ProfileRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            data=serializer.data
        )

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

@extend_schema(tags=['Auth'])
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)

