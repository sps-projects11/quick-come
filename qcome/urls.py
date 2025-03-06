from django.urls import path
from . import views
[
    # Home
    path('', views.HomeView.as_view(), name='home'),
]