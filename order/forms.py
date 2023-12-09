import datetime

from django import forms
from django.utils.datastructures import MultiValueDict

from order.models import STATUSES, Order

SORTING = [('-created', 'Новые'), ('created', 'Старые'), ('end_date', 'По дате возврата')]
ADMIN_SORTING = [(('-created', 'Новые'), ('created', 'Старые'), ('end_date', 'По дате возврата'))]

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

DAYS = (
    (today, 'Сегодня'),
    (tomorrow, 'Завтра'),
)

ARCHIVE = (
    ('True', 'Только архивные'),
    ('All', 'Все'),
    ("False", 'Без архивных'),
)


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


class SortForm(forms.Form):
    def __init__(self, data, **kwargs):
        initial = kwargs.get("initial", {})
        data = MultiValueDict({**{k: [v] for k, v in initial.items()}, **data})
        super().__init__(data, **kwargs)

    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер заказа или фамилию получателя'
    }))
    sort = forms.CharField(
        widget=forms.Select(choices=SORTING, attrs={
            'class': 'form-control form-select',
            'onChange': 'form.submit();',
        }),
    )
    status = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=STATUSES)
    start_date = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS)
    end_date = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DAYS)
    archived = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=ARCHIVE)
