from django.urls import path
from .views import products_list, product_detail, category_products, products_search, user_profile, campaign

urlpatterns = [
    path('product/list/', products_list, name='products_list'),
    path('product/detail/<int:pk>/', product_detail, name='product_detail'),
    path('product/search/', products_search, name='product_search'),
    path('category/<int:pk>/products/', category_products, name='product_detail'),
    path('profile/', user_profile, name='user_profile'),
    path('campaign/', campaign, name='camping')

]
