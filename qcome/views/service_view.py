from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from qcome.services import service_service,workers_service,garage_service
from ..decorators import auth_required, role_required
from ..constants import Role

class ServiceListView(View):
    def get(self, request):
        """Returns a list of active services."""
        services = service_service.get_services_for_cart()
        return JsonResponse({"services": list(services)}, status=200)

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class ServiceCatalogueView(View):
    def get(self, request):
        services = service_service.get_all_service_details()
        is_worker=workers_service.is_user_a_garage_worker(request.user.id)
        is_garage = garage_service.is_user_a_garage_owner(request.user.id)
        if is_worker:
            return render(request, 'worker/services.html', {"services": services}) 
        if is_garage:
            return render(request, 'garage/services.html', {"services": services}) 
        return render(request, 'enduser/services.html', {"services": services}) 