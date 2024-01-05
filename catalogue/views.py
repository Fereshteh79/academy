from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Product, Category


def products_list(request):
    products = Product.objects.prefetch_related('category').all()
    context = "\n".join([f"{product.title}, {product.upc}" for product in products])
    return HttpResponse(context)


def product_detail(request, pk):
    product = get_object_or_404(Product, Q(pk=pk) | Q(upc=pk), is_active=True)
    return HttpResponse(f"title: {product.title}")


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


@login_required()
@require_http_methods(request_method_list=["GET"])
@user_passes_test(check_is_active)
@user_passes_test(lambda u: u.is_staff)
@permission_required('transaction.has_score_permission')
def user_profile(request):
    return HttpResponse(f"Hello{request.user.username}")


@login_required()
@require_POST
@user_passes_test(lambda u: u.score > 20)
@user_passes_test(lambda u: u.age > 14)
def campaign(request):
    return HttpResponse(f"Hello {request.user.username}")
