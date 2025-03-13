from ..models import Booking, ServiceCatalog,Work
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





def update_booking(user, booking_id, current_location, vehicle_type, service_id, description):
    """Allow user to update their booking instead of blocking them."""
    try:
        booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
        service = ServiceCatalog.objects.get(id=int(service_id))  # Validate service

        booking.current_location = current_location
        booking.vehicle_type = vehicle_type
        booking.service = service
        booking.description = description
        booking.updated_by = user  # Track who updated it
        booking.save()
        
        return booking
    except Booking.DoesNotExist:
        return "not_found"  
    except ServiceCatalog.DoesNotExist:
        return "invalid_service"  
    except Exception:
        return "error"


def delete_booking(user, booking_id):
    """Soft delete a booking (only if the user owns it)."""
    try:
        booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
        booking.delete()  # Hard delete instead of soft delete
        return "deleted"
    except Booking.DoesNotExist:
        return "not_found"
    except Exception:
        return "error"


def get_booking_worker(worker_id):
    return list(Work.objects.filter(work_by=worker_id))

def get_booking_by_id(user_id):
    return Booking.objects.filter(customer=user_id).first() 