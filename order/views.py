from datetime import datetime
from decimal import Decimal

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from books.models import Basket, Book
from common.views import TitleMixin
from order.forms import OrderForm, OrderUpdateForm, SortForm
from order.models import CANCELED, Order


class OrderListView(TitleMixin, ListView):
    model = Order
    template_name = 'order/orders.html'
    title = 'Library - Мои заказы'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset().filter(user=self.request.user)

        sort = self.request.GET.get('sort')
        if sort:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-created')

        status = self.request.GET.getlist('status')
        if status:
            queryset = queryset.filter(status__in=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['form'] = SortForm(self.request.GET)
        return context


class OrderDetailView(TitleMixin, DetailView):
    template_name = 'order/order.html'
    title = 'Library - Мои заказ'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        return context


def order_cancel(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.user == request.user and order.status != CANCELED:
        for order_book in order.books:
            book = Book.objects.get(id=order_book.get('book_id'))
            book.copies += 1
            book.save()
        order.status = CANCELED
        order.archived = True
        order.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name = 'order/order-create.html'
    title = 'Library - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('order:orders')
    success_message = 'Поздравляем Ваш заказ принят в работу!'

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
    order = Order.objects.filter(id=pk).first()
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

    def get_queryset(self):
        archived = self.request.GET.get('archived')
        if archived == 'True':
            queryset = super().get_queryset().filter(archived=True).order_by('-created')
        elif archived == 'All':
            queryset = super().get_queryset().order_by('-created')
        else:
            queryset = super().get_queryset().filter(archived=False).order_by('-created')

        if not self.request.GET:
            return queryset

        # Фильтрация
        filters = Q()
        options = ['status', 'start_date', 'end_date']
        for key in options:
            value = self.request.GET.getlist(key)
            if value:
                filters &= Q(**{f'{key}__in': value})
            queryset = queryset.filter(filters)

        # Сортировка
        sort = self.request.GET.get('sort')
        if sort:
            queryset = queryset.order_by(sort)

        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(id__icontains=search) | Q(last_name__icontains=search))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdminPageView, self).get_context_data(**kwargs)
        form = SortForm(self.request.GET, initial={'archived': 'False'})
        context['form'] = form
        return context


class AdminUpdateOrderView(TitleMixin, UpdateView):
    model = Order
    template_name = 'order/admin-update-order.html'
    success_url = reverse_lazy('order:admin-list')
    form_class = OrderUpdateForm
    title = 'Library - Администратор'

    def get_initial(self):
        initial = super().get_initial()
        initial['start_date'] = self.object.start_date.strftime('%Y-%m-%d')
        initial['end_date'] = self.object.end_date.strftime('%Y-%m-%d')
        initial['status'] = self.object.status
        return initial

    def post(self, request, *args, **kwargs):
        self.objects = self.get_object()
        status = self.request.POST.get('status')
        if status in ['3', '5']:
            for order_book in self.object.books:
                book = Book.objects.get(id=order_book.get('book_id'))
                book.copies += 1
                book.save()
            self.object.archived = True
            self.object.save()
        return super(AdminUpdateOrderView, self).post(request, **kwargs)
