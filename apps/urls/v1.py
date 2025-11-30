from django.urls import path, include

urlpatterns = [
    path('users/', include('apps.users.urls.v1', namespace='users')),
    path('cars/', include('apps.cars.urls.v1', namespace='cars')),
    # path('stories/', include('apps.stories.urls.v1', namespace='stories')),
    path('hotels/', include('apps.hotels.urls.v1', namespace='hotels')),
    # path('stories/', include('apps.stories.urls.v1', namespace='stories')),
    # path('cart/', include('apps.cart.urls.v1', namespace='cart')),
]
