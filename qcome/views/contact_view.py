from django.views import View
from django.shortcuts import render, redirect
from qcome.services import workers_service,garage_service

class ContactView(View):
    def get(self,request):
        is_worker=workers_service.is_user_a_garage_worker(request.user.id)
        is_garage = garage_service.is_user_a_garage_owner(request.user.id)
        if is_worker:
            return render(request, 'worker/Contact/index.html')
        elif is_garage:
            return render(request, 'garage/Contact/index.html')
        return render(request, 'enduser/Contact/index.html')