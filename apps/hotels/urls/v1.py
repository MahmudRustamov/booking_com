from django.urls import path
from apps.users.views.nana import home_view

app_name = 'cars'

urlpatterns = [
    path('', home_view, name='home'),
]
