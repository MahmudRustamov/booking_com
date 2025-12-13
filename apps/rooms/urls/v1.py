from django.urls import path
from apps.rooms.views.room_list_view import RoomListCreateApiView
from apps.rooms.views.room_detail_view import RoomDetailApiView

app_name = 'rooms'
urlpatterns = [
    path('', RoomListCreateApiView.as_view(), name='room-list-create'),
    path('<int:pk>/', RoomDetailApiView.as_view(), name='room-detail'),
]
