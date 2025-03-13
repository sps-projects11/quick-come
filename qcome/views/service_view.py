from django.http import JsonResponse
from django.views import View
from ..models import ServiceCatalog

class ServiceListView(View):
    def get(self, request):
        """Returns a list of active services."""
        services = ServiceCatalog.objects.filter(is_active=True).values("id", "service_name")
        return JsonResponse({"services": list(services)}, status=200)
