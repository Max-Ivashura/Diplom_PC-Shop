from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Список товаров
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),  # Фильтр по категории
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Детальная страница товара
    path('compare/', views.comparison_view, name='comparison_view'),
    path('add_to_comparison/<int:product_id>/', views.add_to_comparison, name='add_to_comparison'),
    path('remove_from_comparison/<int:product_id>/', views.remove_from_comparison, name='remove_from_comparison'),
]