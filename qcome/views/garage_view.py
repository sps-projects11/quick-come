from django.shortcuts import render
from django.views import View

from qcome.services.garage_service import get_garage_details
from ..services import get_garage_bookings


class GarageCreateView(View):
    def get(self, request, garage_id):
        garage_details = get_garage_details(garage_id)  # Fetch garage details
        context = {
            'garage_details': garage_details,
            'user': request.user,
        }
        return render(request, 'enduser/Profile/garage/garage_profile_create.html', context)



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

             
