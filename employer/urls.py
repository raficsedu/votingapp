from django.urls import path

from . import views

urlpatterns = [
    # API
    path('api/employer/list', views.employer_list, name='employer_list')
]
