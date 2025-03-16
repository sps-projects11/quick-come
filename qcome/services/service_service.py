from ..models import User, ServiceCatalog

def service_List():
    return ServiceCatalog.objects.filter(is_active=True).all()

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

 