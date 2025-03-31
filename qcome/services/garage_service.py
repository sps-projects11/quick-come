from ..models import Garage, Booking, ServiceCatalog,Work
from ..services import workers_service,work_service
from qcome.constants.default_values import Vehicle_Type,Status

def get_garage_bookings():
    """ Get all active bookings that are not assigned """
    queryset = Booking.objects.filter(is_active=True, assigned_worker=None).order_by('-created_at')
    # Convert queryset to a list to allow modification
    bookings = list(queryset)

    for booking in bookings:
        booking.status=work_service.get_status_of_work(booking.id)
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


def get_garage_list():
    """ Get all garages """
    return Garage.objects.filter(is_active = True)


def is_user_a_garage_owner(user):
    """ Check if the user owns a garage """
    return Garage.objects.filter(garage_owner=user, is_active=True).exists()


def get_garage(worker_garage):
    return Garage.objects.get(id=worker_garage, is_active = True)


def get_garage_id(user_id):
    return Garage.objects.get(garage_owner=user_id)


def toggle_garage_status(garage):
    try:
        garage = Garage.objects.get(id=garage)
    except Garage.DoesNotExist:
        return None
    
    garage.is_active = not garage.is_active
    garage.save()

    return garage


def garage_create(user, garage_name, garage_profile_photo_path, address, phone, vehicle_type, garage_ac, created_by):
    return Garage.objects.create(
        garage_owner=user,
        garage_name=garage_name,
        garage_image=garage_profile_photo_path,
        address=address,
        phone=phone,
        vehicle_type=vehicle_type,
        garage_ac=garage_ac,
        is_active=True,  # Make sure new garages are active
        created_by=created_by
    )


def garage_update(garage_id, user, garage_name, address, phone, garage_ac, garage_vehicle_type, garage_profile_photo_path):
    try:
        garage = Garage.objects.get(id=garage_id)
    except Garage.DoesNotExist:
        return None
    
    garage.garage_name = garage_name
    garage.garage_image = garage_profile_photo_path
    garage.address = address
    garage.phone = phone
    garage.vehicle_type = garage_vehicle_type
    garage.garage_ac = garage_ac
    garage.updated_by = user

    garage.save()
    return garage


def get_all_garage_works(garage):
    workers = workers_service.get_all_worker_of_garage(garage)
    queryset = Booking.objects.filter(assigned_worker__in=workers).order_by('-created_at')
    bookings = []

    if queryset:
        bookings = [
            {
                'id':booking.id,
                'customer_name': f"{booking.customer.first_name} {booking.customer.last_name}",
                'description':booking.description,
                'customer_phone': booking.customer.phone,
                'services': list(ServiceCatalog.objects.filter(id__in=booking.service).values_list("service_name", flat=True)),
                'assigned_worker': f"{booking.assigned_worker.worker.first_name} {booking.assigned_worker.worker.last_name}",
                'vehicle_type':Vehicle_Type(booking.vehicle_type).name,
                'current_location':booking.current_location,
            }
            for booking in queryset
        ]

        # Adding formatted service names
        for booking in bookings:
            booking['service_name'] = services_name(booking["services"])    
            booking['status'] = Status(booking_status(booking["id"])).name if booking_status(booking["id"]) is not None else None
    return bookings  # Return the modified list

def services_name(services):
    return ", ".join(services) if services else "No service"

def booking_status(booking_id):
    status = Work.objects.filter(booking=booking_id).values_list('status', flat=True)
    return status.first() if status else None  # Return the first status if available


def get_all_garages_exclude_worker_garage(worker_garage):
    return Garage.objects.exclude(id=worker_garage)
