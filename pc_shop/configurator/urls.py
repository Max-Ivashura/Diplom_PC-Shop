from django.urls import path
from . import views

urlpatterns = [
    path('', views.configurator_view, name='configurator'),  # Главная страница конфигуратора
    path('save/', views.save_build, name='save_build'),  # Сохранение сборки
    path('build/<int:pk>/', views.build_detail, name='build_detail'),  # Детальная страница сборки
]