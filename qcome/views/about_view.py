from django.views import View
from qcome.services import garage_service,workers_service
from django.shortcuts import render


class AboutView(View):
    def get(self,request):
        is_worker=workers_service.is_user_a_garage_worker(request.user.id)
        is_garage = garage_service.is_user_a_garage_owner(request.user.id)
        if is_worker:
            return render(request, 'worker/About/index.html')
        elif is_garage:
            return render(request, 'garage/About/index.html')
        return render(request, 'enduser/About/index.html')