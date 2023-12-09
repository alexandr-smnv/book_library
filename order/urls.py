from django.urls import path

from order.views import (AdminPageView, AdminUpdateOrderView, OrderCreateView,
                         OrderDetailView, OrderListView, order_cancel,
                         update_data, update_data_admin)

app_name = 'order'

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name='order-create'),
    path("", OrderListView.as_view(), name='orders'),
    path('update_data/', update_data, name='update_data'),
    path('update_data_admin/<int:pk>', update_data_admin, name='update_data_admin'),
    path("cancel/<int:order_id>/", order_cancel, name='order-cancel'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('admin/', AdminPageView.as_view(), name='admin-list'),
    path('admin-update/<int:pk>', AdminUpdateOrderView.as_view(), name='admin-update'),
]
