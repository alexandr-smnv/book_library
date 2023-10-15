from datetime import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from order.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию'
    }))
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'date_start',
        'class': 'form-control py-4 date-c',
        'placeholder': 'Начало аренды'
    }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'date_end',
        'class': 'form-control py-4 date-c',
        'placeholder': 'Окончание аренды'
    }))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'start_date', 'end_date')
