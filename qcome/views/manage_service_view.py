from django.views import View
from django.shortcuts import render, redirect
from ..services import service_service, user_service
from ..constants import Role
from ..decorators import auth_required, role_required
from qcome.package.file_management import save_uploaded_file
from django.contrib import messages  # For user feedback
from ..package.response import success_response,error_response
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class ManageServiceList(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        service = service_service.service_List()
        return render(request, 'adminuser/service_catalog/service_catalog.html',{'services':service, 'admin':admin_data})


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class ManageServiceCreate(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        return render(request, 'adminuser/service_catalog/service_catalog_from.html', {'admin':admin_data})
    
    def post(self, request):
        user = request.user        
        service_name = request.POST.get('service_name', '')
        spare_part = request.POST.get('spare_part', '')
        price = request.POST.get('price', '')
        
        service_image_file = request.FILES.get('service_image')
        service_image_path = save_uploaded_file(service_image_file, 'service-catalog-image')
        
        # Save the service record using your service_create helper function
        service_service.service_create(user, service_name, service_image_path, spare_part, price)
        messages.success(request, SuccessMessage.S00011.value)
        return redirect('manage_service_list')


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class ManageServiceUpdate(View):
    def get(self, request, service_id):
        admin_data = user_service.get_user(request.user.id)
        service = service_service.get_service(service_id)
        return render(request, 'adminuser/service_catalog/service_update.html', {'service': service, 'admin': admin_data})
    
    def post(self, request, service_id):
        user = request.user
        service = service_service.get_service(service_id)
        service_name = request.POST.get('service_name')
        spare_part = request.POST.get('spare_part', '')
        price = request.POST.get('price')
        
        service_image_file = request.FILES.get('service_image')
        service_image_path = save_uploaded_file(service_image_file, 'service-catalog-image')
        
        # Save the service record using your service_create helper function
        service_service.service_update(service, user, service_name, service_image_path, spare_part, price)
        messages.success(request, SuccessMessage.S00012.value)
        return redirect('manage_service_list')


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class ManageServiceDelete(View):
    def post(self, request, service_id):
        service_service.remove_service(service_id, request.user)
        messages.success(request, SuccessMessage.S00013.value)
        return redirect('manage_service_list')
    
        