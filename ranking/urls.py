from django.urls import path

from . import views

app_name = 'ranking'

urlpatterns = [
    path('subs', views.rank_by_subscribers, name='rank_by_subscribers'),
    path('views', views.rank_by_viewers, name='rank_by_viewers'),
]
