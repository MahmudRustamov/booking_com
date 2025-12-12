from django.urls import path
from apps.rooms.views import RoomListCreateApiView, RoomDetailApiView

urlpatterns = [
    path('', RoomListCreateApiView.as_view(), name='room-list-create'),
    path('<int:pk>/', RoomDetailApiView.as_view(), name='room-detail'),
]
