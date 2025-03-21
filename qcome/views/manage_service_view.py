from django.views import View
from django.shortcuts import render, redirect
from ..services import service_service 
from ..constants import Role
from django.http import HttpResponse
from qcome.package.file_management import save_uploaded_file

class ManageServiceList(View):
    def get(self, request):
        service = service_service.service_List()
        return render(request, 'adminuser/service_catalog/service_catalog.html',{'services':service})
    

class ManageServiceListCreate(View):
    def get(self, request):
        return render(request, 'adminuser/service_catalog/service_catalog_from.html')
    
    def post(self, request):
        user = request.user
        if user.roles in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
            service_name = request.POST.get('service_name', '')
            spare_part = request.POST.get('spare_part') or None
            price = request.POST.get('price', '')
            
            service_image_file = request.FILES.get('service_image')
            service_image_path = save_uploaded_file(service_image_file, 'service-catalog-image')
            
            # Save the service record using your service_create helper function
            service_service.service_create(user, service_name, service_image_path, spare_part, price)
            return redirect('manage_service_list')
        else:
            return HttpResponse("Unauthorized", status=403)



class ManageServiceListUpdate(View):
    def get(self, request, service_id):
        return


class ManageServiceListDelete(View):
    def post(self, request, service_id):
        return
    
        