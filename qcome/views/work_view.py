from django.views import View
from django.shortcuts import render
from ..services import booking_service,garage_service
from ..constants.default_values import Vehicle_Type
from qcome.decorators import auth_required, role_required


class WorkListView(View):
    def get(self, request):
        bookings = booking_service.get_booking_worker(request.user.id)
        booking_data = []
        if bookings:
            booking_data = [{
                'booking_id': booking.id,
                'customer_id': f"{booking.customer.first_name} {booking.customer.last_name}",
                'customer_photo': booking.customer.profile_photo_url,
                'address':booking.current_location,
                'service':booking.service.service_name,
                'vehicle_type': Vehicle_Type(booking.vehicle_type).name  # Fix Enum access
            } for booking in bookings]

        print(booking_data)
        return render(request,'worker/work/work_list.html')
    

class WorkUpdate(View):
    def get(self, request, booking_id):
        return
    
    def post(self, request, booking_id):
        return
    

@auth_required(login_url='/sign-in/')
class AllWorkListView(View):
    def get(self,request):
        garage= garage_service.get_garage_id(request.user.id)
        works=garage_service.get_all_garage_works(garage)
        print(works)
        return render(request,'garage/all_work_list.html',{'bookings':works})