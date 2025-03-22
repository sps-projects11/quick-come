from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, workers_service,booking_service


class HomeView(View):
    def get(self, request):
        user=request.user.id if request.user.is_authenticated else None
        garage = garage_service.is_user_a_garage_owner(user)
        worker = workers_service.is_user_a_garage_worker(user)

        if garage:
            garage = garage_service.get_garage_id(request.user.id)
            workers = workers_service.get_worker_of_garage(garage.id)
            workers_list = [{"id": worker.id, "name": f"{worker.worker.first_name} {worker.worker.last_name}"} for worker in workers] 
            bookings = garage_service.get_garage_bookings()
            return render(request, 'garage/bookings.html', {'garage':garage,'bookings':bookings,'workers': workers_list})
        elif worker:
            worker_id=workers_service.get_worker_id(user)
            works = booking_service.get_bookings(worker_id.id)
            return render(request, 'worker/work/work_list.html', {'bookings':works})
        else:
            return render(request, 'enduser/home/index.html', {'user':user})

    
class ChangeMyThemeView(View):
    def post(self, request):
        return
        
