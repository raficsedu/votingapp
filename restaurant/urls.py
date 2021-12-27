from django.urls import path

from . import views

urlpatterns = [
    # API
    path('api/restaurant/list', views.restaurant_list, name='restaurant_list'),
    path('api/restaurant/menu/list', views.menu_list, name='menu_list'),
]
