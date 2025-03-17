from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from qcome.services import service_service

class ServiceListView(View):
    def get(self, request):
        """Returns a list of active services."""
        services = service_service.get_services_for_cart()
        return JsonResponse({"services": list(services)}, status=200)

class ServiceCatalogueView(View):
    def get(self, request):
        services = service_service.get_all_service_details()
        print(services)  # Debugging print statement        
        return render(request, 'enduser/services.html', {"services": services}) 