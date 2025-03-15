from ..models import Garage, Booking

def get_garage_bookings():
    """ Get all active bookings that are not assigned """
    return Booking.objects.filter(is_active=True, assigned_worker=None).order_by('-created_at')

def get_booking_details(booking_id):
    """ Get a single booking """
    return Booking.objects.get(id=booking_id)

def get_garage_details(garage_id):
    """ Get details of a specific garage """
    return Garage.objects.filter(id=garage_id).first()

def get_garage_list():
    """ Get all garages """
    return Garage.objects.all()

def create_garage(garage_owner, garage_data):
    """ Create a new garage for a user """
    return Garage.objects.create(garage_owner=garage_owner, **garage_data)

def update_garage(garage_id, garage_data):
    """ Update an existing garage """
    Garage.objects.filter(id=garage_id).update(**garage_data)

def delete_garage(garage_id):
    """ Delete a garage """
    Garage.objects.filter(id=garage_id).delete()

def is_user_a_garage_owner(user):
    """ Check if the user owns a garage """
    return Garage.objects.filter(garage_owner=user, is_active=True).exists()
