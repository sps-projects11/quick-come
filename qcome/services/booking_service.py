from ..models import Booking, ServiceCatalog,Work
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404


def get_booking_list():
    """Fetch all active bookings."""
    return Booking.objects.filter(is_active=True)


def create_booking(user, current_location, vehicle_type, service_id, description):
    """Allow only one active booking per user."""
    try:
        # Check if the user already has an active booking
        if Booking.objects.filter(customer=user, is_active=True).exists():
            return False  # Indicating booking is already present
        
        # Ensure service_id is valid
        service = get_object_or_404(ServiceCatalog, id=service_id)

        # Create a new booking
        booking = Booking.objects.create(
            customer=user,
            current_location=current_location,
            vehicle_type=vehicle_type,
            service=[service.id],  # Pass the actual service object
            description=description,
            created_by=user,
            updated_by=user
        )
        return booking

    except:
        return "error"




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
    try:
        booking = Booking.objects.get(id=booking_id, is_active=True)
        service_ids = booking.service  # This is a list of service IDs

        services = ServiceCatalog.objects.filter(id__in=service_ids).values(
            'service_name', 'service_image', 'price'
        )

        service_data = list(services)
        return service_data

    except Booking.DoesNotExist:
        return []


def remove_service_from_booking(booking_id, service_name):
    """
    Removes a service from a booking's service list if the service exists.
    """
    try:
        # Get the active service
        service = ServiceCatalog.objects.filter(service_name=service_name, is_active=True).first()
        if not service:
            return {"success": False, "error": "Service not found"}

        # Get the active booking
        booking = Booking.objects.filter(id=booking_id, is_active=True).first()
        if not booking:
            return {"success": False, "error": "Booking not found"}

        # Ensure the service ID exists in the ArrayField
        if service.id not in booking.service:
            return {"success": False, "error": "Service not linked to this booking"}

        # Remove the service ID from the list
        booking.service.remove(service.id)
        
        # Update the booking record
        booking.save(update_fields=["service"])

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

        # Ensure the service ID is not already in the booking's service list
        if service.id in booking.service:
            return {"success": False, "error": "Service already added to booking"}

        # Append the new service ID to the list
        booking.service.append(service.id)
        
        # Save the updated booking
        booking.save(update_fields=["service"])

        return {"success": True, "message": "Service added successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

def total_price(services):
    return sum(service["price"] for service in services)
