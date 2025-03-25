from django.urls import re_path
from .consumers import BookingConsumer, WorkerAssignmentConsumer

websocket_urlpatterns = [
    re_path(r"ws/booking_updates/$", BookingConsumer.as_asgi()),
    re_path(r"ws/worker-assignments/$", WorkerAssignmentConsumer.as_asgi()),
]
