from ..models import User, ServiceCatalog

def service_List():
    return ServiceCatalog.objects.filter(is_active=True).all()

def get_service(service_id):
    return ServiceCatalog.objects.get(id=service_id, is_active=True)

def service_create(user,service_name, service_image, spare_part, price):
    ServiceCatalog.objects.create(
        service_name = service_name,
        service_image = service_image,
        spare_part = spare_part,
        price = price,
        created_by = user,
    )

def get_services_for_cart():
    return ServiceCatalog.objects.filter(is_active=True).values("id", "service_name")

def get_all_service_details():
    return list(ServiceCatalog.objects.filter(is_active=True).values('id','service_name','service_image','price'))


def service_update(service, user, service_name, service_image, spare_part, price):
    service.service_name = service_name
    service.service_image = service_image
    service.spare_part = spare_part
    service.price = price
    service.updated_by = user
    service.save()



def remove_service(service_id, user):
    service = ServiceCatalog.objects.get(id=service_id, is_active=True)
    service.is_active = False
    service.updated_by = user
    service.save()


 