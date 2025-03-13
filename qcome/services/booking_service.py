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
    return Booking.objects.filter(customer=user_id,is_active=True).first() 

def get_services_by_id(booking_id):
    services = Booking.objects.filter(
        id=booking_id, is_active=True
    ).select_related('service').values(
        'service__service_name', 
        'service__service_image', 
        'service__price'
    )

    service_data = [
        {
            'service_name': service['service__service_name'],
            'service_image': service['service__service_image'],
            'service_price': service['service__price'],
        }
        for service in services
    ]
    return service_data


def remove_service_from_booking(booking_id, service_name):
    """
    Removes a service from a booking if the service is linked.
    """
    try:
        # Get the active service
        service = ServiceCatalog.objects.filter(service_name=service_name, is_active=True).first()
        if not service:
            return {"success": False, "error": "Service not found"}

        # Get the active booking linked to this service
        booking = Booking.objects.filter(id=booking_id, service=service, is_active=True).first()
        if not booking:
            return {"success": False, "error": "Booking not found or not linked to the service"}

        # Delete the booking
        booking.delete()
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

def add_service_to_booking(booking_id, service_id):
    """
    Adds a service to a booking without removing existing services.
    """
    try:
        # Get the service
        service = ServiceCatalog.objects.filter(id=service_id, is_active=True).first()
        if not service:
            return {"success": False, "error": "Service not found"}

        # Get the active booking
        booking = Booking.objects.filter(id=booking_id, is_active=True).first()
        if not booking:
            return {"success": False, "error": "Booking not found"}

        # Ensure the service is not already in the booking
        if booking.services.filter(id=service_id).exists():
            return {"success": False, "error": "Service already added to booking"}

        # Add the new service
        booking.services.add(service)
        booking.save()

        return {"success": True, "message": "Service added successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}