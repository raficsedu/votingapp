from django.urls import path

from . import views

urlpatterns = [
    # API
    path('api/vote/list', views.employer_vote, name='employer_vote'),
    path('api/vote/result', views.vote_result, name='vote_result'),
]
