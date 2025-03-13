from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import booking_service,service_service

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BillingHomeView(View):
    def get(self, request):
        booking_id = booking_service.get_booking_by_id(request.user.id)
        services = booking_service.get_services_by_id(booking_id.id)
        
        # Calculate total price in Python
        total_price = sum(service["service_price"] for service in services)
        
        return render(request, 'enduser/Booking/cart.html', {
            'booking_id': booking_id, 
            'services': services,
            'total_price': total_price  # Pass computed total to the template
        })



class BillingUpdate(View):
    def get(self, request, billing_id):
        return
    
    def post(self, request, billing_id):
        return
    