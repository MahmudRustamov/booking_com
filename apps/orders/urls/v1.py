from django.urls import path

from apps.orders.views.order_detail_view import RoomOrderDetailApiView
from apps.orders.views.order_list_veiw import RoomOrderListCreateApiView

app_name = 'orders'

urlpatterns = [
    path('rooms/', RoomOrderListCreateApiView.as_view(), name='room-orders-list-create'),
    path('rooms/<int:pk>/', RoomOrderDetailApiView.as_view(), name='room-order-detail'),
]