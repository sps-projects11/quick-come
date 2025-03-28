from django.urls import re_path
from .consumers import BookingConsumer, WorkerAssignmentConsumer,BookingListAllConsumer,PaymentConsumer,WorkerUpdateConsumer,GarageBillConsumer

websocket_urlpatterns = [
    re_path(r"ws/bookings/$", BookingListAllConsumer.as_asgi()),
    re_path(r"ws/booking_updates/$", BookingConsumer.as_asgi()),
    re_path(r"ws/worker-assignments/$", WorkerAssignmentConsumer.as_asgi()),
     re_path(r"^ws/payments/user_(?P<user_id>\d+)/$",PaymentConsumer.as_asgi()),  # For payment updates
    re_path(r'ws/workers/$', WorkerUpdateConsumer.as_asgi()), 
    re_path(r"ws/garage_bills/$", GarageBillConsumer.as_asgi()),
]
