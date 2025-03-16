from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_builds, name='community_builds'),  # Лента сборок
    path('build/<int:pk>/', views.community_build_detail, name='community_build_detail'),  # Детальная страница сборки
    path('publish/', views.publish_build, name='publish_build'),  # Публикация сборки
]