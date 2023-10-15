from datetime import datetime

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from books.models import Basket
from common.views import TitleMixin
from order.forms import OrderForm


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order/order-create.html'
    title = 'Library - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('books:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['start_date'] = datetime.today().date()
        return initial

    def form_valid(self, form):
        baskets = Basket.objects.filter(user=self.request.user)
        price = sum([basket.price_on_day() for basket in baskets]) * (form.cleaned_data['end_date'] - form.cleaned_data['start_date']).days
        books = [basket.de_json() for basket in baskets]
        form.instance.user = self.request.user
        form.instance.books = books
        form.instance.price = price
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def update_data(request):
    baskets = Basket.objects.filter(user=request.user)
    start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
    delta = (end_date - start_date).days + 1
    price = sum([basket.price_on_day() for basket in baskets]) * delta

    data = {'total_price': price}
    return JsonResponse(data)
