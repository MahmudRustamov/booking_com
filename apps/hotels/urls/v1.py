from django.urls import path

from apps.hotels.views.hotel_detail_view import HotelDetailApiView
from apps.hotels.views.hotels_list_view import HotelListCreateApiView

app_name = 'hotels'

urlpatterns = [
    path('', HotelListCreateApiView.as_view(), name='list-create'),
    path('<int:pk>/', HotelDetailApiView.as_view(), name='detail'),
]
