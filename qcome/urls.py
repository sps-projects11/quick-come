from django.urls import path
from . import views

urlpatterns = [  # ✅ Ensure urlpatterns is properly defined
    path('', views.HomeView.as_view(), name='home'),
]
