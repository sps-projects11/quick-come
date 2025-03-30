from qcome.models import Work,ServiceCatalog,Booking
from qcome.constants.default_values import Status

def work_create(booking,work_by,user):
    return Work.objects.create(
        booking = booking,
        customer = user,
        work_by = work_by,
        status = Status.ACCEPTED.value
    )

def get_work_by_id(work_id):
    work = Work.objects.filter(id=work_id,is_active=True).first()
    work_data={}
    if work:
        work_data={
            'id':work.id,
            'customer_name':f"{work.customer.first_name} {work.customer.last_name}",
            'status': Status(work.status).name,
            'location':work.booking.current_location,
            'services':list(ServiceCatalog.objects.filter(id__in=work.booking.service).values(
                'service_name', 'service_image', 'price'
            )),
        }
    return work_data

def update_work_status(work_id, work_status):
    work = Work.objects.filter(id=work_id).first()
    
    if work:
        # Ensure status is a valid choice, you might have a status enum
        work.status = work_status
        work.save()  # Save changes
        return True
    print("false")
    
    return False


def get_statuss_work_id():
    statuss = []
    
    # Iterate over the specific status values you want (e.g., 4, 5, 6)
    for status_value in [3, 4, 5, 6]:
        if Status(status_value):  # If valid in the Status Enum
            statuss.append({
                'id': status_value,
                'name': Status(status_value).name,  # Get status name
            })
    return statuss

def is_work_complete(booking_id):
    result=Work.objects.filter(booking=booking_id,is_active=True,status=Status.COMPLETED.value)
    if result:
        return True
    return False

def is_work_status_updatable(work_id):
    res = Work.objects.filter(
        id=work_id, 
        is_active=True, 
        status__in=[Status.ACCEPTED.value, Status.WORKING.value]  # Use `status__in`
    )
    return res.exists()  # Returns True if any records match, otherwise False

def get_status_of_work(booking_id):
    booking=Booking.objects.filter(id=booking_id).first()
    status="NOT_STARTED"
    if booking.assigned_worker:
        is_work=Work.objects.filter(booking=booking_id,is_active=True).exists()
        if is_work:
            work=Work.objects.filter(booking=booking_id,is_active=True).first()
            status = Status(work.status).name
            return status
    return status

def get_work_id(booking_id):
    work = Work.objects.filter(booking=booking_id,is_active=True).first()
    work_id = work.id
    return work_id

