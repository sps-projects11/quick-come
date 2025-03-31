from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from qcome.constants.default_values import Role, Vehicle_Type,PayStatus
from qcome.decorators import auth_required, enduser_required,garage_required
from qcome.services import booking_service, garage_service,workers_service,payment_service
from qcome.models import Garage
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from qcome.package.file_management import save_uploaded_file
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


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
            messages.success(request, SuccessMessage.S00008.value)
            return redirect('garage_profile')
        else:
            messages.error(request, ErrorMessage.E00013.value)
            return redirect('user_profile')


@auth_required(login_url='/sign-in/')
@garage_required
class GarageProfileView(View):
    def get(self, request):
        """ Display the garage profile for the logged-in user """
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect if not logged in

        # Fetch only active garages for the user
        garages = Garage.objects.filter(garage_owner=request.user, is_active=True)

        if not garages.exists():
            messages.error(request, "No active garage found.")
            return redirect('garage_create')  # Redirect to create a new garage

        # If multiple active garages exist, pick the first one
        garage = garages.first()
        owner_name = garage.garage_owner.get_full_name() or garage.garage_owner.email

        # Mapping vehicle type integer values to readable names
        vehicle_type_mapping = {
            Vehicle_Type.CAR.value: "Car",
            Vehicle_Type.BIKE.value: "Bike",
            Vehicle_Type.BOTH.value: "Car & Bike",
        }

        # Ensure the correct name is fetched
        vehicle_type_name = vehicle_type_mapping.get(int(garage.vehicle_type), "Unknown")


        context = {
            'garage': garage,
            'garage_owner': owner_name,
            'vehicle_type_name': vehicle_type_name,  # Send the mapped name
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
                    'worker_name': f"{worker.worker.first_name} {worker.worker.last_name}",
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
        """ Load the same create page but pre-fill it for update """
        garage = get_object_or_404(Garage, id=garage_id, garage_owner=request.user)
        vehicle_types = [(v_type.value, v_type.name) for v_type in Vehicle_Type]
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', {'garage': garage, 'vehicle_types': vehicle_types})

    def post(self, request, garage_id):
        """ Update existing garage details """
        garage = get_object_or_404(Garage, id=garage_id, garage_owner=request.user)

        garage.garage_name = request.POST.get('garage_name')
        garage.address = request.POST.get('address')
        garage.phone = request.POST.get('phone')
        garage.vehicle_type = request.POST.get('vehicle_type')
        garage.garage_ac = request.POST.get('garage_ac')

        # Handle image update
        garage_profile_photo = request.FILES.get('garage_image')

        garage_profile_photo_path = ''

        if garage_profile_photo:
            garage_profile_photo_path = save_uploaded_file(garage_profile_photo, subfolder="garage-profile-photo")

        garage.garage_image = garage_profile_photo_path

        garage.updated_by = request.user
        garage.save()

        messages.success(request, "Garage updated successfully!")
        return redirect('garage_profile')


@auth_required(login_url='/sign-in/')
@garage_required
class GarageDeleteView(View):
    def post(self, request, garage_id):
        """ Delete garage and redirect to home page """
        garage = get_object_or_404(Garage, id=garage_id, garage_owner=request.user)
        garage.is_active = False  # ✅ Mark as inactive
        garage.save()
        messages.success(request, "Garage deleted successfully!")
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