from django.urls import path

from order.views import OrderCreateView, update_data

app_name = 'order'

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name='order-create'),
    path('update_data/', update_data, name='update_data'),
]
