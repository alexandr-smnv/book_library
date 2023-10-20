from django import forms

from order.models import Order, STATUSES


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


class OrderUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя',
        'readonly': True,
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию',
        'readonly': True,
    }))
    start_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'date_start',
        'class': 'form-control py-4 date-c',
        'placeholder': 'Начало аренды',
    }))
    end_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'id': 'date_end',
        'class': 'form-control py-4 date-c',
        'placeholder': 'Окончание аренды',
    }))
    status = forms.IntegerField(
        widget=forms.Select(choices=STATUSES, attrs={
            'class': 'form-control form-select',
        })
    )

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'start_date', 'end_date', 'status',)
