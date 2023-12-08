from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = 'details'

urlpatterns = [
    path('details/<str:ytb>', views.details, name='details'),
]