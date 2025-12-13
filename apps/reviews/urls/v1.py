from django.urls import path
from apps.reviews.views.reviews_detail_view import HotelReviewDetailApiView, RoomReviewDetailAPIView
from apps.reviews.views.reviews_list_view import HotelReviewListCreateApiView, RoomReviewListCreateAPIView

app_name = 'reviews'

urlpatterns = [
    path('hotels/', HotelReviewListCreateApiView.as_view(), name='hotel-review-list-create'),
    path('hotels/<int:pk>/', HotelReviewDetailApiView.as_view(), name='hotel-review-detail'),
    path('rooms/<int:room_id>/', RoomReviewListCreateAPIView.as_view(), name='room-review-list-create'),
    path('rooms/detail/<int:room_id>/', RoomReviewDetailAPIView.as_view(), name='room-review-detail'),

]
