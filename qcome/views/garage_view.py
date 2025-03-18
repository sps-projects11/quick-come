import os
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage

from qcome.models.garage_workers_model import Worker
from ..models import Garage
from ..constants import Vehicle_Type
from qcome.services import booking_service


class GarageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        """ Show the create garage form, or redirect to update if the garage already exists """
        existing_garage = Garage.objects.filter(garage_owner=request.user).first()
        if existing_garage:
            return redirect('garage_update', garage_id=existing_garage.id)

        vehicle_types = [(v_type.value, v_type.name) for v_type in Vehicle_Type]
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', {'vehicle_types': vehicle_types})

    def post(self, request):
        """ Create a garage for the logged-in user (Only one allowed) """
        existing_garage = Garage.objects.filter(garage_owner=request.user).first()
        if existing_garage:
            messages.error(request, "You can only create one garage.")
            return redirect('garage_profile', garage_id=existing_garage.id)

        garage_name = request.POST.get('garage_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        garage_ac = request.POST.get('garage_ac')

        # Handle image upload
        garage_image = request.FILES.get('garage_image')
        file_url = None
        if garage_image:
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'static/all-Pictures/'))
            filename = fs.save(garage_image.name, garage_image)
            file_url = f"/static/all-Pictures/{filename}"

        garage = Garage.objects.create(
            garage_owner=request.user,
            garage_name=garage_name,
            garage_image=file_url,
            address=address,
            phone=phone,
            vehicle_type=vehicle_type,
            garage_ac=garage_ac,
            created_by=request.user,
            updated_by=request.user,
        )

        messages.success(request, "Garage created successfully!")
        return redirect('garage_profile', garage_id=garage.id)


class GarageProfileView(View):
    def get(self, request, garage_id):
        """ Display the garage profile """
        garage = get_object_or_404(Garage, id=garage_id)
        owner_name = garage.garage_owner.get_full_name() or garage.garage_owner.email

        context = {
            'garage': garage,
            'garage_owner': owner_name,
        }
        return render(request, 'garage/garage_profile.html', context)


class GarageWorkerListView(View):
    def get(self, request):
        workers = Worker.objects.all()
        return render(request, 'garage/workers.html')

    def post(self, request):
        return None


class GarageUpdateView(LoginRequiredMixin, View):
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
        garage_image = request.FILES.get('garage_image')
        if garage_image:
            fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'static/all-Pictures/'))
            filename = fs.save(garage_image.name, garage_image)
            garage.garage_image = f"/static/all-Pictures/{filename}"

        garage.updated_by = request.user
        garage.save()

        messages.success(request, "Garage updated successfully!")
        return redirect('garage_profile', garage_id=garage.id)


class GarageDeleteView(LoginRequiredMixin, View):
    def post(self, request, garage_id):
        """ Delete garage and redirect to home page """
        garage = get_object_or_404(Garage, id=garage_id, garage_owner=request.user)
        garage.delete()
        messages.success(request, "Garage deleted successfully!")
        return redirect('garage_create')
    

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