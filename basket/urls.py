from django.urls import path
from .views import add_to_basket

urlpatterns = [
    path('add/', add_to_basket, name='add_to_basket')
]