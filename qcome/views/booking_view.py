from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role
from django.contrib import messages
from ..models import Booking,ServiceCatalog
from ..services import booking_service, user_service
from ..decorators import auth_required, role_required
from qcome.constants.default_values import Vehicle_Type,Status
from django.contrib import messages 
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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
@method_decorator(csrf_exempt, name='dispatch')
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
            'user_name': user_service.user_full_name(user),
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
                        "customer_name": user_service.user_full_name(user),
                        "customer_phone": booking.customer.phone,
                        "vehicle_type": Vehicle_Type(int(booking.vehicle_type)).name,
                        "current_location": booking.current_location,
                        "services":booking_service.get_booking_service(booking.service),
                        "description": booking.description,
                        "status": "NOT_STARTED", 
                    },
                },
            )

            messages.success(request, SuccessMessage.S00017.value)
            return redirect('home')

        messages.error(request, ErrorMessage.E00021.value)
        return redirect('booking_create')


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
@method_decorator(csrf_exempt, name='dispatch')
class BookingUpdateView(View):
    def get(self, request, booking_id):
        """Show the booking form with existing booking data for update."""
        user = request.user
        try:
            booking = Booking.objects.get(id=booking_id, customer=user)  # Ensure user owns it
            services = ServiceCatalog.objects.filter(is_active=True)  # Get active services

            return render(request, 'enduser/Booking/booking_create.html', {  # Reuse booking_create.html
                'user_name': user_service.user_full_name(user),
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
            messages.error(request, ErrorMessage.E00023.value)
        elif result == "invalid_service":
            messages.error(request, ErrorMessage.E00021.value)
        elif result == "error":
            messages.error(request, ErrorMessage.E00022.value)
        else:
            messages.success(request, SuccessMessage.S00018.value)

        return redirect('booking_list')


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
@method_decorator(csrf_exempt, name='dispatch')
class BookingDeleteView(View):
    def post(self, request, booking_id):
        """Handle booking delete request."""
        user = request.user
        result = booking_service.delete_booking(user, booking_id)

        if result == "not_found":
            messages.error(request, ErrorMessage.E00023.value)
        elif result == "error":
            messages.error(request, ErrorMessage.E00022.value)
        else:
            messages.success(request, SuccessMessage.S00019.value)

        return redirect('home')
       