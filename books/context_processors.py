from books.models import Basket


def baskets(request):
    user = request.user
    user_baskets = Basket.objects.filter(user=user) if user.is_authenticated else []
    basket_ids = {basket.book_id: basket.id for basket in user_baskets}

    return {
        'baskets': user_baskets,
        'basket_ids': basket_ids
    }
