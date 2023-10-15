from django.contrib import admin

# Register your models here.
from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'status', 'price', 'expired')