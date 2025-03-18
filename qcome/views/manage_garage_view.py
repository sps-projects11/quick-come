from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from django.http import JsonResponse
from qcome.constants.default_values import Vehicle_Type
import os
from quickcome import settings
import hashlib
from django.contrib import messages  # For user feedback


class ManageGarageListView(View):
    def get(self, request):
        garages = garage_service.get_garage_list()

        for garage in garages:
            # Compute the vehicle type string if needed.
            garage.vehicle = Vehicle_Type(garage.vehicle_type).name if garage.vehicle_type else "N/A"
            # Construct the owner's full name.
            garage.garage_owner_name = (
                f"{garage.garage_owner.first_name} "
                f"{(garage.garage_owner.middle_name + ' ') if garage.garage_owner.middle_name else ''}"
                f"{garage.garage_owner.last_name}"
            )

        # Pass the list of garage objects to the template.
        return render(request, 'adminuser/garage/garage_list.html', {'garages': garages})

    
class ManageGarageCreateView(View):
    def get(self, request):
        available_users = user_service.get_non_garage_and_non_worker_users()
        print(available_users)
        return render(request, 'adminuser/garage/garage_create.html', {'available_garage':available_users})

    def post(self, request):        
        user = user_service.get_user(request.user.id)      

        garage_name = request.POST.get('garage_name')
        garage_owner = request.POST.get('garage_owner')
        address = request.POST.get('garage_address')
        phone = request.POST.get('garage_phone')
        garage_ac = request.POST.get('garage_ac')        
        garage_vehicle_type = request.POST.get('vehicle_type')
        garage_profile_photo = request.FILES.get('garage_profile_photo')

        garage_profile_photo_path = ''

        if garage_profile_photo:
            garage_profile_photo_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'garage-profile-photo')
            if not os.path.exists(garage_profile_photo_dir):
                os.makedirs(garage_profile_photo_dir)

            md5_hash = hashlib.md5()
            for chunk in garage_profile_photo.chunks():
                md5_hash.update(chunk)
            file_hash = md5_hash.hexdigest()

            _, ext = os.path.splitext(garage_profile_photo.name)
            new_file_name = f"{file_hash}{ext}"
            file_path = os.path.join(garage_profile_photo_dir, new_file_name)

            if not os.path.exists(file_path):
                garage_profile_photo.seek(0)
                with open(file_path, 'wb+') as destination:
                    for chunk in garage_profile_photo.chunks():
                        destination.write(chunk)

            garage_profile_photo_path = f'/static/all-Pictures/garage-profile-photo/{new_file_name}'        

        garage = garage_service.garage_create( garage_owner, garage_name, garage_profile_photo_path, address, phone, garage_vehicle_type, garage_ac, user)
        if garage is None:
            messages.error(request, ErrorMessage.E00014.value)
            return redirect('manage_garages_list')
        
        messages.success(request, SuccessMessage.S00007.value)
        return redirect('manage_garages_list')




    

class ManageGarageUpdateView(View):
    def get(self, request, garage_id):
        garage = garage_service.get_garage(garage_id)

        return render(request, 'adminuser/garage/garage_update.html', {'garage':garage})
    
    def post(self, request, garage_id):
        user = user_service.get_user(request.user.id)      

        garage_name = request.POST.get('garage_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        garage_ac = request.POST.get('garage_ac')        
        garage_vehicle_type = request.POST.get('garage_vehicle_type')
        garage_profile_photo = request.FILES.get('garage_profile_photo')

        garage_profile_photo_path = ''

        if garage_profile_photo:
            garage_profile_photo_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'garage-profile-photo')
            if not os.path.exists(garage_profile_photo_dir):
                os.makedirs(garage_profile_photo_dir)

            md5_hash = hashlib.md5()
            for chunk in garage_profile_photo.chunks():
                md5_hash.update(chunk)
            file_hash = md5_hash.hexdigest()

            _, ext = os.path.splitext(garage_profile_photo.name)
            new_file_name = f"{file_hash}{ext}"
            file_path = os.path.join(garage_profile_photo_dir, new_file_name)

            if not os.path.exists(file_path):
                garage_profile_photo.seek(0)
                with open(file_path, 'wb+') as destination:
                    for chunk in garage_profile_photo.chunks():
                        destination.write(chunk)

            garage_profile_photo_path = f'/static/all-Pictures/garage-profile-photo/{new_file_name}'        

        garage = garage_service.garage_update(garage_id, user, garage_name, address, phone, garage_ac, garage_vehicle_type, garage_profile_photo_path)
        if garage is None:
            messages.error(request, ErrorMessage.E00014.value)
            return redirect('manage_garages_list')
        
        messages.success(request, SuccessMessage.S00007.value)
        return redirect('manage_garages_list')
    

class ManageGarageToggleView(View):
    def post(self, request, garage_id):
        garage = garage_service.toggle_garage_status(garage_id)

        if garage is None:
            return JsonResponse(error_response(ErrorMessage.E00013.value))
        
        return JsonResponse(success_response(SuccessMessage.S00006.value))