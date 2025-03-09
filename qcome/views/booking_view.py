from django.views import View
from django.shortcuts import render, redirect
class BookingListView(View):
    def get(self,request):
        return render(request, 'enduser/booking.html')
    
class BookingCreateView(View):
    def get(self,request):
        return
    def post(self,request):
        return
    
class BookingUpdateView(View):
    def get(self,request):
        return
    def post(self,request):
        return
    
class BookingDeleteView(View):
    def get(self,request):
        return
    def post(self,request):
        return
