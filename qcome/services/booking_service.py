from ..models import Booking

def get_booking_list():
    bookings=Booking.objects.all()
    return bookings

def create_booking(booking_id):
    Booking.objects.create()
    return 

def update_booking(booking_id):
    Booking.objects.update()
    return

def delete_booking(booking_id):
    Booking.objects.update()
    return