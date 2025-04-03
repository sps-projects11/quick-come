from django.views import View
from django.shortcuts import render
from ..services import booking_service, garage_service, user_service
from ..constants.default_values import Vehicle_Type
from qcome.decorators import auth_required, garage_required, worker_required


@auth_required(login_url='/sign-in/')
@worker_required
class WorkListView(View):
    def get(self, request):
        bookings = booking_service.get_booking_worker(request.user.id)
        booking_data = []
        if bookings:
            booking_data = [{
                'booking_id': booking.id,
                'customer_id': user_service.user_full_name(booking.customer),
                'customer_photo': booking.customer.profile_photo_url,
                'address':booking.current_location,
                'service':booking.service.service_name,
                'vehicle_type': Vehicle_Type(booking.vehicle_type).name  # Fix Enum access
            } for booking in bookings]
        return render(request,'worker/work/work_list.html')

    

@auth_required(login_url='/sign-in/')
@garage_required
class AllWorkListView(View):
    def get(self,request):
        garage= garage_service.get_garage_id(request.user.id)
        works=garage_service.get_all_garage_works(garage)
        return render(request,'garage/all_work_list.html',{'bookings':works})

  
    