from ..models import Booking, ServiceCatalog
from django.db.utils import IntegrityError

def get_booking_list():
    """Fetch all active bookings."""
    return Booking.objects.filter(is_active=True)

def create_booking(user, current_location, vehicle_type, service_id, description):
    """Allow only one booking per user."""
    try:
        service_id = int(service_id)
        service = ServiceCatalog.objects.get(id=service_id)

        # Check if the user already has ANY booking (active or inactive)
        if Booking.objects.filter(customer=user).exists():
            return "already_exists"  # Indicate that the user already booked

        # Create a new booking
        booking = Booking.objects.create(
            customer=user,
            current_location=current_location,
            vehicle_type=vehicle_type,
            service=service,
            description=description,
            created_by=user,
            updated_by=user
        )
        return booking

    except ServiceCatalog.DoesNotExist:
        return None  # Service does not exist
    except (ValueError, Exception):
        return "error"  # Handle unexpected errors

def update_booking(booking_id, data):
    """Update an existing booking."""
    try:
        booking = Booking.objects.get(id=booking_id)
        for key, value in data.items():
            setattr(booking, key, value)
        booking.save()
        return booking
    except Booking.DoesNotExist:
        return None  # Handle this in the view

def delete_booking(booking_id):
    """Soft delete a booking by marking it inactive."""
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.is_active = False
        booking.save()
        return booking
    except Booking.DoesNotExist:
        return None  # Handle this in the view
