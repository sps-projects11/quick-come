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
    path('admin/dashboard', views.AdminHomeView.as_view(), name='admin_dashboard'),

    # Admin-User Management
    path('admin/users/', views.ManageUsersListView.as_view(), name='manage_users'),
    path('admin/users/create', views.ManageUsersCreateView.as_view(), name='manage_user_create'),
    path('admin/<int:user_id>/profile', views.ManageUserUpdateView.as_view(), name='manage_user_update'),
    path('admin/<int:user_id>/profile/toggle', views.ManageUserToggleView.as_view(), name='manage_user_toggle'),

    # Admin-Garage Management
    path('admin/garage/', views.ManageGarageListView.as_view(), name='manage_garages_list'),
    path('admin/garage/create', views.ManageGarageCreateView.as_view(), name='manage_garage_create'),
    path('admin/garage/<int:garage_id>/update', views.ManageGarageUpdateView.as_view(), name='manage_garage_update'),
    path('admin/<int:garage_id>/garage/toggle', views.ManageGarageToggleView.as_view(), name='manage_garage_toggle'),

    # Admin-Worker Management
    path('admin/worker/', views.ManageWorkerListView.as_view(), name='manage_worker_list'),
    path('admin/worker/create', views.ManageWorkerCreateView.as_view(), name='manage_worker_create'),   
    path('admin/worker/<int:worker_id>/update', views.ManageWorkerUpdateView.as_view(), name='manage_worker_update'),
    path('admin/worker/<int:worker_id>/toggle', views.ManageWorkerToggleView.as_view(), name='manage_worker_toggle'),

    # Admin-Service Management
    path('admin/service/', views.ManageServiceList.as_view(), name='manage_service_list'),
    path('admin/service/create', views.ManageServiceListCreate.as_view(), name='manage_service_create'),
    path('admin/service/<int:service_id>/update', views.ManageServiceListUpdate.as_view(), name='manage_service_update'),
    path('admin/service/<int:service_id>/toggle', views.ManageServiceListDelete.as_view(), name='manage_service_delete'),

    # Admin-Payment Management
    path('admin/payments', views.ManagePaymentListView.as_view(), name='manage_payment_list'),

    # Theme
    path('change-my-theme/', views.ChangeMyThemeView.as_view(), name='change_my_theme'),

   
 #GARAGE ----------------------------------------------------------------------->
    # Garage
    path('garage/create/', views.GarageCreateView.as_view(), name='garage_create'),
    path('garage/profile/', views.GarageProfileView.as_view(), name='garage_profile'),
    path('garage/update/<int:garage_id>/', views.GarageUpdateView.as_view(), name='garage_update'),
    path('garage/delete/<int:garage_id>/', views.GarageDeleteView.as_view(), name='garage_delete'),
    path('garage/work_list/', views.AllWorkListView.as_view(), name='garage_work_list'),
    path('garage/workers/', views.GarageWorkerListView.as_view(), name='garage_workers_list'),
    path('worker/asigned/', views.AssignedWorkerCreateView.as_view(), name='worker_assign_create'),
    #Garage bills
    path('garage/bills/', views.GarageBillsListView.as_view(), name='garage_bills'),
    path('garage/bills/<int:booking_id>/', views.GarageBillReceipeView.as_view(), name='garage_bill_reciepe'),


 #WORKER ----------------------------------------------------------------------->
    # Work
    path('work/', views.WorkListView.as_view(), name='work'),
    # Billing
    path('billing/', views.BillingHomeView.as_view(), name='billing,'),
    path('billing/<int:booking_id>/update', views.BillingUpdate.as_view(), name='billing_update'),
    path('billing/<int:booking_id>/delete', views.BillingDelete.as_view(), name='billing_update'),
    #Payment
    path('payment/',views.PaymentListView.as_view(), name='payment_list'),
    path('payment/create/<int:booking_id>/',views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment/receipt/<int:payment_id>/', views.PaymentReceipt.as_view(), name='payment_receipt'),
    # Workers
    path('worker/',views.WorkerView.as_view(),name='worker'),
    path('worker/<int:user_id>/create/',views.WorkerCreateView.as_view(),name='worker_create'),
    path('worker/<int:worker_id>/update/',views.WorkerUpdateView.as_view(),name='worker_update'),
    path('worker/<int:worker_id>/delete/',views.WorkerDeleteView.as_view(),name='worker_delete'),
    path('worker/payments/', views.WorkerPaymentListView.as_view(), name='worker_payments'),
    path('services/list/', views.ServiceListView.as_view(), name='list_service'),
    path('work/<int:work_id>/', views.WorkerWorkRecieptView.as_view(), name='worker_work_details'),

    path("api/check-worker/", views.CheckWorkerStatus.as_view(), name='check_worker_status'),

    
 ##ENDUSER ----------------------------------------------------------------------------------------->

    # User-Profile
    path('profile/', views.EnduserProfileView.as_view(), name='user_profile'),
    path('profile/<int:user_id>/update/', views.EnduserProfileUpdate.as_view(), name='profile_update' ),
    path('profile/<int:user_id>/delete/', views.EnduserProfileDelete.as_view(), name='profile_delete' ),
    #Booking
    path('booking/',views.BookingListView.as_view(), name='booking_list'),
    path('booking/<int:booking_id>/',views.BookingDetailView.as_view(), name='booking_details'),
    path('booking/create/',views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/update/<int:booking_id>/',views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/delete/<int:booking_id>/',views.BookingDeleteView.as_view(), name='booking_delete'),
    path('services/', views.ServiceCatalogueView.as_view(), name='list_service_catalouge'),

    #--------------------------------------------------------------------------------->

     #Contact
    path('contact/',views.ContactView.as_view(), name='contact'),

    #About
    path('about/',views.AboutView.as_view(), name='about'),


]

