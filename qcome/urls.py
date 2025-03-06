from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    path('sign-in/', views.UserSigninView.as_view(), name='sign_in'),

    # Admin
    path('admin/', views.AdminHomeView.as_view(), name='admin'),
    path('admin/dashboard', views.AsminDashboard.as_view(), name='admin_dashboard'),

    # Admin-Profile Management
    path('admin/users/', views.ManageUsersListView.as_view(), name='manage_users'),
    path('admin/<int:user_id>/profile', views.ManageUserProfile.as_view(), name='manage_user'),
    path('admin/service/', views.ManageServiceList.as_view(), name='manage_service_list'),
    path('admin/service/create', views.ManageServiceListCreate.as_view(), name='manage_service_create'),
    path('admin/service/<int:service_id>/update', views.ManageServiceListUpdate.as_view(), name='manage_service_update'),
    path('admin/service/<int:service_id>/delete', views.ManageServiceListDelete.as_view(), name='manage_service_delete'),

    # Theme
    path('change-my-theme/', views.ChangeMyThemeView.as_view(), name='change_my_theme'),

    # User-Profile
    path('profile/', views.EnduserProfileView.as_view(), name='user_profile'),
    path('create/profile/', views.EnduserProfileCreate.as_view(), name='profile_create' ),
    path('profile/<int:user_id>/update/', views.EnduserProfileUpdate.as_view(), name='profile_update' ),
    path('profile/<int:user_id>/delete/', views.EnduserProfileDelete.as_view(), name='profile_delete' ),


]
