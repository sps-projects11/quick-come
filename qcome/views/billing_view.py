from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BillingHomeView(View):
    def get(self, request):
        booking_id = 123
        return render(request,'enduser/Booking/cart.html',{'booking_id':booking_id})
    

class BillingUpdate(View):
    def get(self, request, billing_id):
        return
    
    def post(self, request, billing_id):
        return
    