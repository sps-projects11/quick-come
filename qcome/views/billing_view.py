from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role
from ..services import booking_service
from django.http import JsonResponse
import json


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BillingHomeView(View):
    def get(self, request):
        booking = booking_service.get_booking_by_id(request.user.id)  # Get the booking object
        if not booking:
            return render(request, 'enduser/Booking/cart.html')  # No active booking

        services = booking_service.get_services_by_id(booking.id)
        total_price = sum(service["service_price"] for service in services)

        return render(request, 'enduser/Booking/cart.html', {
            'booking_id': booking.id,  # ✅ Ensure it's an integer
            'services': services,
            'total_price': total_price  
        })




class BillingUpdate(View):
    def delete(self, request, booking_id):
        try:
            data = json.loads(request.body)
            service_name = data.get("service_name")

            # Call service layer for deletion
            response = booking_service.remove_service_from_booking(booking_id, service_name)
            
            status_code = 200 if response["success"] else 404
            return JsonResponse(response, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)