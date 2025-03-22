from ..models import Booking, ServiceCatalog, Work
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from qcome.constants.default_values import Vehicle_Type,PayStatus,Status
from qcome.services import payment_service


def get_booking_list(booking_id):
    """Fetch all active bookings with service names."""
    bookings = Booking.objects.filter(id=booking_id)
    if not bookings:
        bookings=[]
        return bookings

    for booking in bookings:
        # Add customer details
        booking.customer_name = f"{booking.customer.first_name} {booking.customer.last_name}"
        booking.customer_phone = booking.customer.phone if booking.customer.phone else "No phone"

        service_ids = booking.service  # List of service IDs
        services = ServiceCatalog.objects.filter(id__in=service_ids).values_list("service_name", flat=True)
        booking.service_names = ", ".join(services) if services else "No service"  # Store as a string
        booking.status= Status(get_booking_status(booking.id)).name
    return bookings

def get_booking_status(booking_id):
    status = Work.objects.filter(booking=booking_id,is_active=True).values('status').first()
    if status:
        status = status['status']
    else:
        status = Status.PENDING.value
    return status

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
    """Allow user to update their booking correctly."""
    try:
        booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
        service = ServiceCatalog.objects.get(id=int(service_id))  # Validate service

        booking.current_location = current_location
        booking.vehicle_type = vehicle_type
        booking.service = [service.id]  # Store service ID in a list
        booking.description = description
        booking.updated_by = user  # Track who updated it
        booking.save()
        
        return booking
    except Booking.DoesNotExist:
        return "not_found"  
    except ServiceCatalog.DoesNotExist:
        return "invalid_service"  
    except Exception as e:
        print("Error:", e)
        return "error"


def delete_booking(user, booking_id):
    """Soft delete a booking (only if the user owns it)."""
    try:
        booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
        booking.is_active = False  # Soft delete by setting is_active to False
        booking.save(update_fields=["is_active"])  # Save the updated field
        return "deleted"
    except Booking.DoesNotExist:
        return "not_found"
    except Exception:
        return "error"


def get_booking_worker(worker_id):
    return list(Work.objects.filter(work_by=worker_id))


def get_booking_by_id(user_id):
    return Booking.objects.filter(assigned_worker__worker_id=user_id,is_active=True).first() 

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
    """Removes a service from a booking's service list if the service exists."""
    try:
        service = ServiceCatalog.objects.filter(service_name=service_name, is_active=True).first()
        if not service:
            return {"success": False, "error": "Service not found"}

        booking = Booking.objects.filter(id=booking_id, is_active=True).first()
        if not booking:
            return {"success": False, "error": "Booking not found"}

        if service.id not in booking.service:
            return {"success": False, "error": "Service not linked to this booking"}

        booking.service.remove(service.id)
        booking.save(update_fields=["service"])

        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}


def add_service_to_booking(booking_id, service_id):
    """Adds a service to a booking without removing existing services."""
    try:
        service = ServiceCatalog.objects.filter(id=service_id, is_active=True).first()
        if not service:
            return {"success": False, "error": "Service not found"}

        booking = Booking.objects.filter(id=booking_id, is_active=True).first()
        if not booking:
            return {"success": False, "error": "Booking not found"}

        if service.id in booking.service:
            return {"success": False, "error": "Service already added to booking"}

        booking.service.append(service.id)
        booking.save(update_fields=["service"])

        return {"success": True, "message": "Service added successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def total_price(services):
    return sum(service["price"] for service in services)


def get_booking(booking_id):
    return Booking.objects.filter(id=booking_id).first()

def get_bills_garage(user_id):
    bookings = Booking.objects.filter(assigned_worker__garage__garage_owner=user_id)
    bills_data = []
    
    if bookings.exists():
        bills_data = [
            {   "booking_id":booking.id,
                "vehicle_type": Vehicle_Type(booking.vehicle_type).name,
                "created_at":booking.created_at,
                "status":PayStatus(payment_service.get_payment_status(booking.id)).name,
                "total": sum(ServiceCatalog.objects.filter(id__in=booking.service).values_list('price', flat=True)),
            }
            for booking in bookings
        ]
    
    return bills_data

def get_bill_details_by_booking_id(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return None  

    bill_data = [{
        "booking_id": booking.id,
        "customer_name": f"{booking.customer.first_name} {booking.customer.last_name}",
        "assigned_worker": f"{booking.assigned_worker.worker.first_name} {booking.assigned_worker.worker.last_name}" if booking.assigned_worker else "Unassigned",
        "services": list(ServiceCatalog.objects.filter(id__in=booking.service).values(
            'service_name', 'service_image', 'price'
        )), 
        "vehicle_type": Vehicle_Type(booking.vehicle_type).name,
        "created_at": booking.created_at.strftime("%d %b %Y, %I:%M %p"),
        "total": sum(ServiceCatalog.objects.filter(id__in=booking.service).values_list('price', flat=True)),  
    }]

    return bill_data 

def get_booking_object(booking_id):
    return Booking.objects.get(id=booking_id)

def get_bookings(worker_id):
    bookings=Booking.objects.filter(assigned_worker=worker_id,is_active=True).values('id','customer__first_name','customer__last_name','vehicle_type','current_location','service','description')
    booking_data=[]
    for booking in bookings:
            booking_data.append({
                'id': booking["id"],
                'customer_name': f"{booking['customer__first_name']} {booking['customer__last_name']}",
                'vehicle_type': Vehicle_Type(booking["vehicle_type"]).value,  # Assuming Vehicle_Type is an Enum
                'current_location': booking["current_location"],
                'description': booking["description"],
                'services': list(ServiceCatalog.objects.filter(id__in=booking["service"]).values(
                    'service_name', 'service_image', 'price'
                ))
            })
    return booking_data


def get_last_5_booking():
    Bookings = Booking.objects.all().order_by('-created_at')[:5]

    for booking in Bookings:
        booking.customer_name = f"{booking.customer.first_name} {booking.customer.last_name}"
        booking.customer_phone = booking.customer.phone if booking.customer.phone else "No phone"
        service_ids = booking.service
        services = ServiceCatalog.objects.filter(id__in=service_ids).values_list("service_name", flat=True)
        booking.service_names = ", ".join(services) if services else "No service"
        booking.vehicle_type = Vehicle_Type(booking.vehicle_type).name


def get_all_booking_list(user):
    """Fetch all active bookings with service names."""
    bookings = Booking.objects.filter(customer=user,is_active=False)

    for booking in bookings:
        # Add customer details
        booking.customer_name = f"{booking.customer.first_name} {booking.customer.last_name}"
        booking.customer_phone = booking.customer.phone if booking.customer.phone else "No phone"

        service_ids = booking.service  # List of service IDs
        services = ServiceCatalog.objects.filter(id__in=service_ids).values_list("service_name", flat=True)
        booking.service_names = ", ".join(services) if services else "No service"  # Store as a string
        booking.status= Status(get_booking_status(booking.id)).name
    return bookings

def get_current_booking(user_id):
    return Booking.objects.filter(customer=user_id,is_active = True).first()
        
