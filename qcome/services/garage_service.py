from ..models import Garage
from ..models import Booking

def get_garage_bookings():
    """
    Get all bookings for the garage owned by the given user.
    """
   
    return Booking.objects.filter(is_active=True, assigned_worker = None).order_by('-created_at')


def get_booking_details(booking_id):
    """
    Get a single booking detail.
    """
    return Booking.objects.get(id=booking_id)


def get_garage_details(garage_id):
    return Garage.objects.filter(id=garage_id).first()





def get_garage_list():
    garages = Garage.objects.all()
    return garages

def create_garage_list(garage_id):
    Garage.objects.create()
    return

def update_garage_list(garage_id):
    Garage.objects.update()
    return

def delete_garage_list(garage_id):
    Garage.objects.delete()
    return


def is_user_a_garage_owner(user):
    return Garage.objects.filter(garage_owner=user, is_active=True).exists()
