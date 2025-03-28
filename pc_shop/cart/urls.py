from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),  # Корзина
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Добавление товара
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # Удаление товара
]