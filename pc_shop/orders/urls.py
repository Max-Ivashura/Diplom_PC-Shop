from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),  # Оформление заказа
    path('order/<int:pk>/', views.order_detail, name='order_detail'),  # Детали заказа
]