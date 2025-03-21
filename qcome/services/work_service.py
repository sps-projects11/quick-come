from qcome.models import Work,ServiceCatalog
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
    print(work_data)
    return work_data


