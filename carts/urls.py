from django.urls import path

from greatcart import views
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
]