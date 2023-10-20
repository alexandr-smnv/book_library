from decimal import Decimal
from datetime import datetime

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from books.models import Basket
from common.views import TitleMixin
from order.forms import OrderForm, OrderUpdateForm
from order.models import Order


class OrderListView(TitleMixin, ListView):
    template_name = 'order/orders.html'
    title = 'Library - Мои заказы'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    template_name = 'order/order.html'
    title = 'Library - Мои заказ'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order/order-create.html'
    title = 'Library - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('books:index')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['start_date'] = datetime.today().strftime('%Y-%m-%d')
        return initial

    def form_valid(self, form):
        baskets = Basket.objects.filter(user=self.request.user)
        books = []
        for basket in baskets:
            basket.reduction_quantity()
            books.append(basket.de_json())
        form.instance.user = self.request.user
        form.instance.books = books
        baskets.delete()
        return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def update_data(request):
    baskets = Basket.objects.filter(user=request.user)
    start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
    delta = (end_date - start_date).days + 1
    price = sum([basket.book.price_on_day() for basket in baskets]) * delta

    data = {'total_price': price}
    return JsonResponse(data)


@csrf_exempt
def update_data_admin(request, pk):
    order = Order.objects.get(id=pk)
    start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
    delta = (end_date - start_date).days + 1

    price = Decimal((sum([book['price'] for book in order.books]) * delta))
    price = price.quantize(Decimal("1.00"))

    data = {'total_price': price}
    return JsonResponse(data)


class AdminPageView(TitleMixin, ListView):
    model = Order
    template_name = 'order/admin-page.html'
    title = 'Library - Администратор'
    context_object_name = 'orders'


class AdminUpdateOrderView(TitleMixin, UpdateView):
    model = Order
    template_name = 'order/admin-update-order.html'
    success_url = reverse_lazy('order:admin-list')
    form_class = OrderUpdateForm

    def get_initial(self):
        initial = super().get_initial()
        initial['start_date'] = self.object.start_date.strftime('%Y-%m-%d')
        initial['end_date'] = self.object.end_date.strftime('%Y-%m-%d')
        initial['status'] = self.object.status
        return initial
