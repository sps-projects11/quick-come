from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, workers_service

class HomeView(View):
    def get(self, request):
        user=request.user.id if request.user.is_authenticated else None
        garage = garage_service.is_user_a_garage_owner(user)
        worker = workers_service.is_user_a_garage_worker(user)

        if garage:
            bookings = garage_service.get_garage_bookings()
            print("vcsdh",bookings)
            return render(request, 'garage/bookings.html', {'garage':garage,'bookings':bookings})
        elif worker:
            return render(request, 'worker/index.html', {'worker':worker})
        else:
            return render(request, 'enduser/home/index.html', {'user':user})

    
class ChangeMyThemeView(View):
    def post(self, request):
        return
        
