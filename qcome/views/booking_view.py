from django.views import View
from django.shortcuts import render, redirect
from ..decorators import auth_required, role_required
from ..constants import Role


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class BookingListView(View):
    def get(self,request):
        return
    
@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')    
class BookingCreateView(View):
    def get(self,request):
        user=request.user
        return render(request, 'enduser/Booking/booking.html')
    
    def post(self,request):
        return
    


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
