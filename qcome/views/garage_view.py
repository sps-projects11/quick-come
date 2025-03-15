from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Garage
from ..constants import Vehicle_Type


class GarageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # Pass vehicle type choices to the template
        vehicle_types = [(v_type.value, v_type.name) for v_type in Vehicle_Type]
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', {'vehicle_types': vehicle_types})

    def post(self, request):
        garage_name = request.POST.get('garage_name')
        garage_image = request.FILES.get('garage_image')  # Handle image uploads
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        garage_ac = request.POST.get('garage_ac')

        # Create garage and assign logged-in user as owner
        garage = Garage.objects.create(
            garage_owner=request.user,
            garage_name=garage_name,
            garage_image=garage_image,  # Ensure this works correctly with ImageField
            address=address,
            phone=phone,
            vehicle_type=vehicle_type,
            garage_ac=garage_ac,
            created_by=request.user,
            updated_by=request.user,
        )

        messages.success(request, "Garage created successfully!")
        return redirect('garage_profile', garage_id=garage.id)  # Redirect to the profile page



class GarageProfileView(View):
    def get(self, request, garage_id):
        # Fetch garage details
        garage = get_object_or_404(Garage, id=garage_id)

        context = {
            'garage': garage,
        }
        return render(request, 'garage/garage_profile.html', context)


class GarageUpdateView(View):
    def get(self, request, garage_id):
        return
    def post(self, request, garage_id):
        return

class GarageDeleteView(View):
    def get(self, request, garage_id):
        return
    def post(self, request, garage_id):
        return

             
