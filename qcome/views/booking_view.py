from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from django.contrib import messages
from ..models import Booking,ServiceCatalog
from ..services import booking_service 
from ..decorators import auth_required, role_required
from qcome.constants.default_values import Vehicle_Type,Status

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



# ✅ View to Show Booking History (List of Bookings)
@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingListView(View):
    def get(self, request):
        bookings = booking_service.get_all_booking_list(request.user.id)  # Fetch all bookings
        return render(request, 'enduser/Booking/booking_list.html', {'bookings': bookings})

# ✅ View to Show Booking Details (Specific Booking)
@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingDetailView(View):
    def get(self, request, booking_id):
        booking = booking_service.get_booking_list(booking_id)  # Fetch a specific booking
        return render(request, 'enduser/Booking/booking_details.html', {'bookings': booking})


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')    


class BookingCreateView(View):
    def get(self, request):
        user = request.user
        services = ServiceCatalog.objects.filter(is_active=True)  # Fetch active services
        
        # Get service_id from the URL
        service_id = request.GET.get('service_id')
        selected_service = None
        
        if service_id:
            selected_service = ServiceCatalog.objects.filter(id=service_id, is_active=True).first()

        return render(request, 'enduser/Booking/booking_create.html', {
            'user_name': f"{user.first_name} {user.last_name}",
            'user_phone': user.phone if user.phone else "",  # Default text
            'services': services,  # Pass services to template
            'selected_service': selected_service  # Pass selected service to prefill
        })
    
    def post(self, request):
        user = request.user
        current_location = request.POST.get('current_location')
        vehicle_type = request.POST.get('vehicle_type')
        service_id = request.POST.get('service')
        description = request.POST.get('description')
        phone = request.POST.get('customer_phone')

        booking = booking_service.create_booking(user, current_location, vehicle_type, service_id, description, phone)

        if booking:
            # Emit WebSocket event correctly
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "booking_updates",
                {
                    "type": "send_booking_update",  # Matches method in BookingConsumer
                    "booking": {  # ✅ Correct key
                        "id": booking.id,
                        "customer_name": f"{user.first_name} {user.last_name}",
                        "customer_phone": booking.customer.phone,
                        "vehicle_type": Vehicle_Type(int(booking.vehicle_type)).name,
                        "current_location": booking.current_location,
                        "services":booking_service.get_booking_service(booking.service),
                        "description": booking.description,
                        "status": "NOT_STARTED", 
                    },
                },
            )

            messages.success(request, "Booking created successfully!")
            return redirect('home')

        messages.error(request, "Invalid service selection.")
        return redirect('booking_create')




@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingUpdateView(View):
    def get(self, request, booking_id):
        """Show the booking form with existing booking data for update."""
        user = request.user
        try:
            booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
            services = ServiceCatalog.objects.filter(is_active=True)  # Get active services

            return render(request, 'enduser/Booking/booking_create.html', {  # Reuse booking_create.html
                'user_name': f"{user.first_name} {user.last_name}",
                'user_phone': user.phone if user.phone else "",
                'services': services,
                'booking': booking  # Pass booking object to the form
            })
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found!")
            return redirect('booking_list')  # Redirect to booking list

    def post(self, request, booking_id):
        """Handle booking update request."""
        user = request.user
        current_location = request.POST.get('current_location')
        vehicle_type = request.POST.get('vehicle_type')
        service_id = request.POST.get('service')
        description = request.POST.get('description')

        result = booking_service.update_booking(user, booking_id, current_location, vehicle_type, service_id, description)

        if result == "not_found":
            messages.error(request, "Booking not found!")
        elif result == "invalid_service":
            messages.error(request, "Invalid service selection!")
        elif result == "error":
            messages.error(request, "Something went wrong!")
        else:
            messages.success(request, "Booking updated successfully!")

        return redirect('booking_list')







@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingDeleteView(View):
    def post(self, request, booking_id):
        """Handle booking delete request."""
        user = request.user
        result = booking_service.delete_booking(user, booking_id)

        if result == "not_found":
            messages.error(request, "Booking not found!")
        elif result == "error":
            messages.error(request, "Something went wrong!")
        else:
            messages.success(request, "Booking deleted successfully!")

        return redirect('home')
       