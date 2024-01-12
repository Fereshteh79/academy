from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.db.models import Q
from .models import Product, Category
from .utils import check_is_active, check_is_staff
from  django.views.decorators.http import require_GET, require_http_methods, require_POST
from  .models import Product, Category, ProductType, Brand
from .utils import check_is_active, check_is_staff


def products_list(request):
    products = Product.objects.prefetch_related('category').all()
    context = dict()
    context['products'] = Product.objects.select_related('category').all()
    context['categories'] = Category.objects.all()
    return render(request, 'catalogue/product_list.html', context=context)


def product_detail(request, pk):
    queryset = Product.objects.filter(is_active=True).filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        form = AddToBasketForm({"product": product.id, 'quantity': 1})
        return render(request, 'catalogue/product_detail.html', {"product": product, "form": form})
    raise Http404


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.filter(is_active=True)
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(context)


def products_search(request):
    title = request.GET.get('q')
    products = Product.objects.filter(is_active=True, title__icontains=title)
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(f"search page:\n{context}")


def user_profile(request):
    return HttpResponse(f"Hello {request.user.username}")


# @login_required()
# @require_http_methods(request_method_list=["GET"])
# @user_passes_test(check_is_active)
# @user_passes_test(lambda u: u.is_staff)
# @permission_required('transaction.has_score_permission')
def user_profile(request):
    return HttpResponse(f"Hello{request.user.username}")


# @login_required()
# @require_POST
# @user_passes_test(lambda u: u.score > 20)
# @user_passes_test(lambda u: u.age > 14)
def campaign(request):
    return HttpResponse(f"Hello {request.user.username}")
