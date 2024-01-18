import django.http
from django.views.decorators.http import require_POST

from .forms import AddToBasketForm
from .models import Basket


@require_POST
def add_to_basket(request):
    # todo_1: check if user has basket_id in cookie
    # todo_2: creat and assign if it doesn't have
    # todo_2_1: check if user is authenticated, set user to the basket
    # todo_3: get product from submitted from
    # todo_4: add product to the user basket lines
    # todo_5: return to the 'next' url
    response = HttpResponseRedirect(request.POST.get('next', '/'))

    basket = Basket.get_basket(request.COOKIES.get('basket_id', None))
    if basket is None:
        raise django.http.Http404

    response.set_cookie('basket_id', basket.id)
    if not basket.validate_user(request.user):
        raise django.http.Http404

    form = AddToBasketForm(request.POST)
    if form.is_valid():
        form.save(basket=basket)

    return response
