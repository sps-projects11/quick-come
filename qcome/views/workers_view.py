from django.views import View
from django.shortcuts import render,redirect
from ..services import *
from ..models import Worker



class GarageWorkerListView(View):
    def get(self, request):
        workers = Worker.objects.all()
        return render(request, 'workers/worker_profile.html', {'workers': workers})

    def post(self, request):
        return None
    

    
class WorkerUpdateView(View):
    def get(self, request, worker_id):
        worker_details = get_worker_details(worker_id)
        context = {'worker_details': worker_details}
        return render(request, 'workers/worker_profile_update.html', context)

    def post(self, request, worker_id):
        worker = get_worker_details(worker_id)
        if worker:
            worker.experience = request.POST.get('experience')
            worker.expertise = request.POST.get('expertise')
            worker.is_verified = request.POST.get('is_verified') == 'on'
            worker.is_active = request.POST.get('is_active') == 'on'
            worker.save()
            return redirect('worker_list')  
        return redirect('worker_list')  
    
class WorkerDeleteView(View):
    def get(self, request, worker_id):
        worker_details = workers_service.get_worker_details(worker_id)
        context = {'worker_details': worker_details}
        return render(request, 'workers/worker_profile_delete.html', context)

    def post(self, request, worker_id):
        worker = workers_service.get_worker_details(worker_id)
        if worker:
            worker.delete()
            return redirect('worker_list')
        return redirect('worker_list')
