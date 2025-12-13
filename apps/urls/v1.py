from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('hotels/', include('apps.hotels.urls.v1', namespace='hotels')),
    path('rooms/', include('apps.rooms.urls.v1', namespace='rooms')),
    path('reviews/', include('apps.reviews.urls.v1', namespace='reviews')),
]
