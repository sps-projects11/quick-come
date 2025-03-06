from django.urls import path
from . import views

urlpatterns = [  # ✅ Ensure urlpatterns is properly defined
    path('', views.HomeView.as_view(), name='home'),

    # Garage paths
    path('garages/', views.GarageListView.as_view(), name='garage_list'),
    path('garages/create/<int:garage_id>/', views.GarageCreateView.as_view(), name='garage_create'),
    path('garages/update/<int:garage_id>/', views.GarageUpdateView.as_view(), name='garage_update'),
    path('garages/delete/<int:garage_id>/', views.GarageDeleteView.as_view(), name='garage_delete'),
]
