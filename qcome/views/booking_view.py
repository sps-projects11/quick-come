from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from django.contrib import messages
from ..models import Booking,ServiceCatalog
from ..services import booking_service 


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingListView(View):
    def get(self,request):
        bookings = booking_service.get_booking_list()
        return render(request, 'enduser/Booking/booking_list.html', {'bookings': bookings})
    



@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')    
class BookingCreateView(View):
    def get(self, request):
        user = request.user
        services = ServiceCatalog.objects.filter(is_active=True)  # Fetch active services
        return render(request, 'enduser/Booking/booking.html', {
            'user_name': f"{user.first_name} {user.last_name}",
            'user_phone': user.phone,
            'services': services  # Pass services to template
        })
    
    def post(self, request):
        user = request.user
        current_location = request.POST.get('current_location')
        vehicle_type = request.POST.get('vehicle_type')
        service_id = request.POST.get('service')
        description = request.POST.get('description')

        booking = booking_service.create_booking(user, current_location, vehicle_type, service_id, description)

        if booking:
            messages.success(request, "Booking created successfully!")
            return redirect('home')  # Redirect to home or another page
        else:
            messages.error(request, "Invalid service selection.")
            return redirect('booking_create')
    


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')  
class BookingUpdateView(View):
    def get(self,request):
        return
    
    def post(self,request):
        return
    


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser') 
class BookingDeleteView(View):
    def get(self,request):
        return
    
    def post(self,request):
        return
