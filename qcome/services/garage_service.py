from ..models import Garage
from ..models import Booking

def get_garage_bookings(garage_owner):
    """
    Get all bookings for the garage owned by the given user.
    """
    garage = Garage.objects.filter(garage_owner=garage_owner).first()
    if not garage:
        return None
    return Booking.objects.filter(is_active=True).order_by('-created_at')

def get_booking_details(booking_id):
    """
    Get a single booking detail.
    """
    return Booking.objects.get(id=booking_id)





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
