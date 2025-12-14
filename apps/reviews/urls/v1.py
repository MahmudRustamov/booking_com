from django.urls import path
from apps.reviews.views.reviews_detail_view import HotelReviewDetailApiView, RoomReviewDetailApiView
from apps.reviews.views.reviews_list_view import HotelReviewListCreateApiView, \
    RoomReviewListCreateApiView

app_name = 'reviews'

urlpatterns = [
    path('hotels/', HotelReviewListCreateApiView.as_view(), name='hotel-review-list-create'),
    path('hotels/<int:pk>/', HotelReviewDetailApiView.as_view(), name='hotel-review-detail'),
    path('rooms/<int:room_id>/reviews/', RoomReviewListCreateApiView.as_view(), name='get-all-reviews'),
    path('rooms/<int:room_id>/reviews/<int:pk>/', RoomReviewDetailApiView.as_view(), name='room-review-detail'),
]
