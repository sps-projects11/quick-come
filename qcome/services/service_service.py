from ..models import User, ServiceCatalog

def service_List():
    return ServiceCatalog.objects.filter(is_active=True).all()