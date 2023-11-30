from django.contrib.auth import logout
from django.urls import path

from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
