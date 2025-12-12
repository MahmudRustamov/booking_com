from django.urls import path
from apps.users.serializers.register import LogoutAPIView
from apps.users.views.auth import RegisterView, VerifyEmailAPIView, VerifyLoginAPIView
from apps.users.views.device import DeviceRegisterCreateAPIView, DeviceListApiView
from apps.users.views.owners import OwnerListCreateApiView, OwnerDetailApiView
from apps.users.views.auth import ProfileRetrieveAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('login/', VerifyLoginAPIView.as_view(), name='login'),
    path('profiles/<int:id>/', ProfileRetrieveAPIView.as_view(), name='user-detail'),
    path('owners/', OwnerListCreateApiView.as_view(), name="owner-list"),
    path('owners/<int:pk>/', OwnerDetailApiView.as_view(), name="owner-detail"),
    path('devices/', DeviceRegisterCreateAPIView.as_view(), name='device-register'),
    path('devices/list/', DeviceListApiView.as_view(), name='device-list'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    # path('profile/', ProfileRetrieveAPIView.as_view(), name='profile'),
]
