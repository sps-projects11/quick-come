from ..models import Garage, Booking, ServiceCatalog

def get_garage_bookings():
    """ Get all active bookings that are not assigned """
    queryset = Booking.objects.filter(is_active=True, assigned_worker=None).order_by('-created_at')

    # Convert queryset to a list to allow modification
    bookings = list(queryset)

    for booking in bookings:
        # Add customer details
        if booking.customer:
            booking.customer_name = f"{booking.customer.first_name} {booking.customer.last_name}"
            booking.customer_phone = getattr(booking.customer, "phone", "No phone")
        else:
            booking.customer_name = "No Customer"
            booking.customer_phone = "No phone"

        # Fetch service names
        service_ids = booking.service  # This is assumed to be a list of IDs
        services = ServiceCatalog.objects.filter(id__in=service_ids).values_list("service_name", flat=True)
        booking.service_names = ", ".join(services) if services else "No service"

    return bookings  # Return modified list


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


def get_garage(worker_garage):

    return Garage.objects.get(id=worker_garage)

def get_garage_id(user_id):
    return Garage.objects.get(garage_owner=user_id)