from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from . import views

urlpatterns = [
    # VIEW
    path('', views.index, name='index'),

    # API
    path('api/authenticate', views.user_authenticate, name='user_authenticate'),
    path('api/logout', views.user_logout, name='user_logout'),
]
