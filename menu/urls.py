from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница (если это нужно в приложении)
    # path('salads/', views.menu_salads, name='menu_salads'),
    # path('soups/', views.menu_soups, name='menu_soups'),
    # path('main_dishes/', views.menu_main_dishes, name='menu_main_dishes'),
    # path('appetizers/', views.menu_appetizers, name='menu_appetizers'),
    # path('garnishes/', views.menu_garnishes, name='menu_garnishes'),
    # path('drinks/', views.menu_drinks, name='menu_drinks'),
    # path('alcohol/', views.menu_alcohol, name='menu_alcohol'),
]
