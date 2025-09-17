from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from django.http import JsonResponse
from qcome.constants.default_values import Vehicle_Type, Role
from qcome.decorators.auth_decorator import auth_required, role_required
from django.contrib import messages  # For user feedback
from qcome.package.file_management import save_uploaded_file
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt



@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
class ManageGarageListView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        garages = garage_service.get_garage_list()

        for garage in garages:
            # Compute the vehicle type string if needed.
            garage.vehicle = Vehicle_Type(garage.vehicle_type).name if garage.vehicle_type else "N/A"
            garage.garage_owner_name = user_service.user_full_name(garage.garage_owner)
            print(garage.garage_owner_name)
        # Pass the list of garage objects to the template.
        return render(request, 'adminuser/garage/garage_list.html', {'garages': garages, 'admin': admin_data})



@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
@method_decorator(csrf_exempt, name='dispatch')
class ManageGarageCreateView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        available_users = user_service.get_non_garage_and_non_worker_users()
        return render(request, 'adminuser/garage/garage_create.html', {'available_garage':available_users, 'admin':admin_data})

    def post(self, request):        
        user = user_service.get_user(request.user.id)      

        garage_name = request.POST.get('garage_name')
        garage_owner_id = request.POST.get('garage_owner')
        address = request.POST.get('garage_address')
        phone = request.POST.get('garage_phone')
        garage_ac = request.POST.get('garage_ac')        
        garage_vehicle_type = request.POST.get('vehicle_type')
        garage_profile_photo = request.FILES.get('garage_profile_photo')

        garage_profile_photo_path = save_uploaded_file(garage_profile_photo, subfolder="garage-profile-photo")

        garage_owner = user_service.get_user(garage_owner_id)
      

        garage = garage_service.garage_create( garage_owner, garage_name, garage_profile_photo_path, address, phone, garage_vehicle_type, garage_ac, user)
        if garage is None:
            messages.error(request, ErrorMessage.E00016.value)
            return redirect('manage_garages_list')
        
        messages.success(request, SuccessMessage.S00008.value)
        return redirect('manage_garages_list')



@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
@method_decorator(csrf_exempt, name='dispatch')
class ManageGarageUpdateView(View):
    def get(self, request, garage_id):
        admin_data = user_service.get_user(request.user.id)
        garage = garage_service.get_garage(garage_id)
        garage_owner = user_service.get_user(garage.garage_owner.id)

        return render(request, 'adminuser/garage/garage_update.html', {'garage':garage, 'admin':admin_data, 'garage_owner':garage_owner})
    
    def post(self, request, garage_id):
        user = user_service.get_user(request.user.id)      

        garage_name = request.POST.get('garage_name')
        garage_owner_first_name = request.POST.get('garage_owner_first_name')
        garage_owner_middle_name = request.POST.get('garage_owner_middle_name', '')
        garage_owner_last_name = request.POST.get('garage_owner_last_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        garage_ac = request.POST.get('garage_ac')        
        garage_vehicle_type = request.POST.get('garage_vehicle_type')
        garage_profile_photo = request.FILES.get('garage_profile_photo')

        garage_profile_photo_path = save_uploaded_file(garage_profile_photo, subfolder="garage-profile-photo")        

        garage = garage_service.garage_update(garage_id, user, garage_name, address, phone, garage_ac, garage_vehicle_type, garage_profile_photo_path)
        garage_owner = user_service.get_user(garage.garage_owner.id)
        user_service.user_name_update(garage_owner, garage_owner_first_name, garage_owner_middle_name, garage_owner_last_name)
        if garage is None:
            messages.error(request, ErrorMessage.E00014.value)
            return redirect('manage_garages_list')
        
        messages.success(request, SuccessMessage.S00007.value)
        return redirect('manage_garages_list')
    


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
@method_decorator(csrf_exempt, name='dispatch')
class ManageGarageToggleView(View):
    def post(self, request, garage_id):
        garage = garage_service.toggle_garage_status(garage_id)

        if garage is None:
            return JsonResponse(error_response(ErrorMessage.E00013.value))
        
        return JsonResponse(success_response(SuccessMessage.S00006.value))
    
    