from ..models import Booking, ServiceCatalog

def get_booking_list():
    """Fetch all active bookings."""
    return Booking.objects.filter(is_active=True)

def create_booking(user, current_location, vehicle_type, service_id, description):
    """Create a new booking for the user."""
    try:
        print(f"Fetching ServiceCatalog with ID: {service_id}")
        service = ServiceCatalog.objects.get(id=int(service_id))  # Convert to integer
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
    except (ServiceCatalog.DoesNotExist, ValueError):
        return None  # Handle this case in the view


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
    

def get_booking_id(user_id):
    return Booking.objects.filter(customer=user_id).first() 
