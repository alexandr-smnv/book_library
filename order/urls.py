from django.urls import path

from order.views import OrderCreateView, update_data, OrderListView

app_name = 'order'

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name='order-create'),
    path("", OrderListView.as_view(), name='orders'),
    path('update_data/', update_data, name='update_data'),
]
