from django.urls import path
from . import views

urlpatterns = [  # ✅ Ensure urlpatterns is properly defined
    path('', views.HomeView.as_view(), name='home'),

    #Booking Paths
    path('booking/',views.BookingListView.as_view(), name='booking_list'),
    path('booking/create/<int:booking_id>/',views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/update/<int:booking_id>/',views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/delete/<int:booking_id>/',views.BookingDeleteView.as_view(), name='booking_delete'),


    #Payment Paths
    path('payment/',views.PaymentListView.as_view(), name='payment_list'),
    path('payment/create/<int:booking_id>/',views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment/update/<int:booking_id>/',views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payment/delete/<int:booking_id>/',views.PaymentDeleteView.as_view(), name='payment_delete'),


    #

]
