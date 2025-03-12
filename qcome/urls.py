from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    path('sign-up/', views.UserSignupView.as_view(), name='sign_up'),
    path('sign-in/', views.UserSigninView.as_view(), name='sign_in'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Authentication
    path('request-otp/', views.RequestOTPView.as_view(), name='request-otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('api/check-login/', views.CheckLoginStatus.as_view(), name='check-login'),

    # Admin
    path('login/admin/', views.LoginAdminView.as_view(), name='login_myadmin'),
    path('log-out/admin/', views.LoginOutAdminView.as_view(), name='logout_myadmin'),
    path('admin/', views.AdminHomeView.as_view(), name='myadmin'),
    path('admin/profile/', views.AdminProfileView.as_view(), name='myadmin_profile'),
    path('admin/profile/update', views.AdminProfileUpdateView.as_view(), name='myadmin_profile_update'),
    path('admin/password/update', views.AdminPasswordUpdateView.as_view(), name='myadmin_password_update'),
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
    path('profile/<int:user_id>/update/', views.EnduserProfileUpdate.as_view(), name='profile_update' ),
    path('profile/<int:user_id>/delete/', views.EnduserProfileDelete.as_view(), name='profile_delete' ),

    # Garage
    path('garages/', views.GarageListView.as_view(), name='garage_list'),
    path('garages/create/', views.GarageCreateView.as_view(), name='garage_create'),
    path('garages/update/<int:garage_id>/', views.GarageUpdateView.as_view(), name='garage_update'),
    path('garages/delete/<int:garage_id>/', views.GarageDeleteView.as_view(), name='garage_delete'),

    #Booking
    path('booking/',views.BookingListView.as_view(), name='booking_list'),
    path('booking/create/',views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/update/<int:booking_id>/',views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/delete/<int:booking_id>/',views.BookingDeleteView.as_view(), name='booking_delete'),

    # Work
    path('work/', views.WorkListView.as_view(), name='work'),
    path('work/<int:booking_id>update', views.WorkUpdate.as_view(), name='work_update'),

    # Billing
    path('billing/', views.BillingHomeView.as_view(), name='billing,'),
    path('billing/<int:billing_id>/update', views.BillingUpdate.as_view(), name='billing_update'),

    #Payment
    path('payment/',views.PaymentListView.as_view(), name='payment_list'),
    path('payment/create/<int:booking_id>/',views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment/receipt/<int:payment_id>/', views.PaymentReceipt.as_view(), name='payment_receipt'),

    # Workers
    path('worker/',views.Worker.as_view(),name='workers'),
    path('worker/<int:worker_id>/update',views.WorkerUpdate.as_view(),name='workers_update'),
    path('worker/<int:worker_id>/delete',views.WorkerDelete.as_view(),name='workers_delete'),

]

