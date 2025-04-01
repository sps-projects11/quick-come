from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from qcome.constants.default_values import Vehicle_Type
from qcome.decorators import auth_required, enduser_required,garage_required
from qcome.services import booking_service, garage_service, workers_service, user_service
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from qcome.package.file_management import save_uploaded_file


@auth_required(login_url='/sign-in/')
@enduser_required
class GarageCreateView(View):
    def get(self, request):
        """ Show the create garage form, or redirect to update if an active garage already exists """
        existing_garage = garage_service.check_existing_garage(request.user)
        if existing_garage:
            garage_service.toggle_garage_status(existing_garage.id)
            return redirect('garage_profile')

        vehicle_types = [(v_type.value, v_type.name) for v_type in Vehicle_Type]
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', {'vehicle_types': vehicle_types})

    def post(self, request):
        """ Create a garage for the logged-in user (Only one allowed) """
        user = request.user
        
        garage_owner_name = request.POST.get('garage_owner_name')
        garage_owner_profile_photo = request.FILES.get('garage_owner_profile_photo')
        garage_name = request.POST.get('garage_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        garage_ac = request.POST.get('garage_ac')
        # Handle image upload
        garage_profile_photo = request.FILES.get('garage_image')

        garage_profile_photo_path = ''

        if garage_profile_photo:
            garage_profile_photo_path = save_uploaded_file(garage_profile_photo, subfolder="garage-profile-photo")

        garage = garage_service.garage_create(user, garage_name, garage_profile_photo_path, address, phone, vehicle_type, garage_ac, user)
        if garage:
            
            garage_owner_profile_photo_path = ''
            if garage_owner_profile_photo:
                garage_owner_profile_photo_path = save_uploaded_file(garage_owner_profile_photo, subfolder="profile-images")

            user_service.user_profile_photo_create(user, garage_owner_profile_photo_path)

            first_name,middle_name, last_name = user_service.split_full_name(garage_owner_name)
            user_service.user_name_update(user, first_name, middle_name, last_name)

            messages.success(request, SuccessMessage.S00008.value)
            return redirect('garage_profile')
        else:
            messages.error(request, ErrorMessage.E00013.value)
            return redirect('user_profile')


@auth_required(login_url='/sign-in/')
@garage_required
class GarageProfileView(View):
    def get(self, request):
        garage = garage_service.get_garage_by_garage_owner(request.user)
        owner_name = user_service.user_full_name(request.user)

        vehicle_type_mapping = {
            Vehicle_Type.CAR.value: "Car",
            Vehicle_Type.BIKE.value: "Bike",
            Vehicle_Type.BOTH.value: "Car & Bike",
        }

        vehicle_type_name = vehicle_type_name = vehicle_type_mapping.get(int(garage.vehicle_type), "Unknown")

        context = {
            'garage': garage,
            'garage_owner': owner_name,
            'garage_owner_image': request.user.profile_photo_url,
            'vehicle_type_name': vehicle_type_name,
        }
        return render(request, 'garage/garage_profile.html', context)



@auth_required(login_url='/sign-in/')
@garage_required
class GarageWorkerListView(View):
    def get(self, request):
        # Fetch garage ID for the current user
        garage_id = garage_service.get_garage_id(request.user.id)
        # Fetch workers in the garage
        workers = workers_service.get_all_worker_of_garage(garage_id)
        # Initialize worker data list
        worker_data = []

        # Ensure we only proceed if there are workers
        if workers:
            worker_data = [
                {
                    'id': worker.id,
                    'worker_name': user_service.user_full_name(worker.worker),
                    'worker_phone': worker.worker.phone,
                    'garage_name': worker.garage.garage_name,
                    'experience': worker.experience,
                    'expertise': worker.expertise,
                    'is_verified': worker.is_verified
                }
                for worker in workers
            ]
        return render(request, 'garage/workers.html', {'workers': worker_data})
    


@auth_required(login_url='/sign-in/')
@garage_required
class GarageUpdateView(View):
    def get(self, request, garage_id):
        garage = garage_service.get_garage(garage_id)
        garage_owner = user_service.get_user(garage.garage_owner.id)
        garage_owner_name = user_service.user_full_name(garage_owner)
        garage_owner_image = user_service.get_user_profile_photo(garage_owner.id)
        context =  {
            'garage': garage,
            'garage_owner_name' : garage_owner_name,
            'garage_owner_image' : garage_owner_image,
        }
        return render(request, 'garage/profile/garage_profile_update.html', context)

    def post(self, request, garage_id):
        garage = garage_service.get_garage(garage_id)
        garage_name = request.POST.get('garage_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        garage_ac = request.POST.get('garage_ac')

        # Handle image update
        garage_profile_photo = request.FILES.get('garage_image')

        garage_profile_photo_path = garage.garage_image

        if garage_profile_photo:
            garage_profile_photo_path = save_uploaded_file(garage_profile_photo, subfolder="garage-profile-photo")
        
        garage = garage_service.garage_update(garage_id, request.user, garage_name, address, phone, garage_ac, vehicle_type, garage_profile_photo_path)

        if garage:
            garage_owner_name = request.POST.get('garage_owner_name')
            garage_owner_profile_photo = request.FILES.get('garage_owner_profile_photo')
            garage_owner_profile_photo_path = request.user.profile_photo_url
            if garage_owner_profile_photo:
                garage_owner_profile_photo_path = save_uploaded_file(garage_owner_profile_photo, subfolder="profile-images")

            user_service.user_profile_photo_create(request.user, garage_owner_profile_photo_path)
            first_name, middle_name, last_name = user_service.split_full_name(garage_owner_name)
            user_service.user_name_update(request.user, first_name, middle_name, last_name)
            messages.success(request, SuccessMessage.S00007.value)
            return redirect('garage_profile')
        else:
            messages.error(request, ErrorMessage.E00014.value)
            return redirect('garage_profile')
            

@auth_required(login_url='/sign-in/')
@garage_required
class GarageDeleteView(View):
    def post(self, request, garage_id):
        garage_service.toggle_garage_status(garage_id)
        messages.success(request, SuccessMessage.S00016.value)
        return redirect('home')
   
     
@auth_required(login_url='/sign-in/')
@garage_required
class GarageBillsListView(View):
    def get(self, request):
        bills_data = booking_service.get_bills_garage(request.user.id)
        return render(request, 'garage/garage_bills.html', {'bills_data': bills_data})



@auth_required(login_url='/sign-in/')
@garage_required    
class GarageBillReceipeView(View):
    def get(self, request, booking_id):
        bill_data = booking_service.get_bill_details_by_booking_id(booking_id)
        # Ensure Decimal values are converted to string for safe rendering
        bill = bill_data[0]
        bill["total"] = str(bill["total"])
        for service in bill["services"]:
            service["price"] = str(service["price"])  # Convert each service price to string
        return render(request, 'garage/garage_bill_receipe.html', {'bill': bill})