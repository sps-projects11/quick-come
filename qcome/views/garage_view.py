import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from qcome.constants.default_values import Role, Vehicle_Type
from qcome.decorators import auth_required, role_required
from qcome.services import booking_service, garage_service,workers_service
import hashlib
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class GarageCreateView(View):
    def get(self, request):
        """ Show the create garage form, or redirect to update if an active garage already exists """
        existing_garage = Garage.objects.filter(garage_owner=request.user, is_active=True).first()
        if existing_garage:
            return redirect('garage_profile')  # Only redirect if it's active

        vehicle_types = [(v_type.value, v_type.name) for v_type in Vehicle_Type]
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', {'vehicle_types': vehicle_types})

    def post(self, request):
        """ Create a garage for the logged-in user (Only one allowed) """
        user = request.user

        existing_garage = Garage.objects.filter(garage_owner=user).first()
        if existing_garage:
            existing_garage.garage_name = request.POST.get('garage_name')
            existing_garage.address = request.POST.get('address')
            existing_garage.phone = request.POST.get('phone')
            existing_garage.vehicle_type = request.POST.get('vehicle_type')
            existing_garage.garage_ac = request.POST.get('garage_ac')
            existing_garage.is_active=True
             # Handle image upload
            garage_profile_photo = request.FILES.get('garage_image')

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
            existing_garage.save()
            return redirect('garage_profile')

        garage_name = request.POST.get('garage_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        garage_ac = request.POST.get('garage_ac')

        # Handle image upload
        garage_profile_photo = request.FILES.get('garage_image')

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

        garage_service.garage_create(user, garage_name, garage_profile_photo_path, address, phone, vehicle_type, garage_ac, user)

        messages.success(request, SuccessMessage.S00008.value)
        return redirect('garage_profile')



@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
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
class GarageWorkerListView(View):
    def get(self, request):
        # Fetch garage ID for the current user
        garage_id = garage_service.get_garage_id(request.user.id)
        print(f"Garage ID: {garage_id}")  # Debugging

        # Fetch workers in the garage
        workers = workers_service.get_worker_of_garage(garage_id)
        print(f"Workers: {workers}")  # Debugging

        # Initialize worker data list
        worker_data = []

        # Ensure we only proceed if there are workers
        if workers:
            worker_data = [
                {
                    'id': worker.id,
                    'worker_name': f"{worker.worker.first_name} {worker.worker.last_name}",
                    'garage_name': worker.garage.garage_name,
                    'experience': worker.experience,
                    'expertise': worker.expertise,
                    'is_verified': worker.is_verified
                }
                for worker in workers
            ]

        print(f"Worker Data: {worker_data}")  # Debugging
        return render(request, 'garage/workers.html', {'workers': worker_data})

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
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

        garage.garage_image = garage_profile_photo_path

        garage.updated_by = request.user
        garage.save()

        messages.success(request, "Garage updated successfully!")
        return redirect('garage_profile')


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class GarageDeleteView(View):
    def post(self, request, garage_id):
        """ Delete garage and redirect to home page """
        garage = get_object_or_404(Garage, id=garage_id, garage_owner=request.user)
        garage.is_active = False  # ✅ Mark as inactive
        garage.save()
        messages.success(request, "Garage deleted successfully!")
        return redirect('home')
    

class GarageBillsListView(View):
    def get(self,request):
        bills_data=booking_service.get_bills_garage(request.user.id)
        return render(request,'garage/garage_bills.html',{'bills_data':bills_data})
    
class GarageBillReceipeView(View):
    def get(self, request, booking_id):
        bill_data = booking_service.get_bill_details_by_booking_id(booking_id)
        # Ensure Decimal values are converted to string for safe rendering
        bill = bill_data[0]
        bill["total"] = str(bill["total"])
        for service in bill["services"]:
            service["price"] = str(service["price"])  # Convert each service price to string
        return render(request, 'garage/garage_bill_receipe.html', {'bill': bill})