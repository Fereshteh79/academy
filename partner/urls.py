from django.urls import path
from .views import products_list, product_detail, category_products, products_search


urlpatterns = [
    path('product/list/', products_list, name='products_list'),
    path('products/search/', products_search, name='products_search'),
    path('product/detail/<int:pk>/', product_detail, name='product_detail'),
    path('category/<int:pk>/products/', category_products, name='category_products'),
]