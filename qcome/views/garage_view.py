from django.shortcuts import render
from django.views import View
from ..services import get_garage_bookings



class GarageCreateView(View):
    def get(self, request):
        user = request.user
        bookings = get_garage_bookings(user)
        print( "jshvjhsvdhj",bookings)

        if bookings is None:
            return render(request, 'garage/bookings.html', {'error': 'No garage found for this user.'})

        return render(request, 'garage/bookings.html', {'bookings': bookings})

    def post(self, request):
        return

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

             
