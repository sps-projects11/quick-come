from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ..services import *
from qcome.models import User, Garage

class Worker(View):
    def get(self, request):
        workers = get_all_workers()
        return render(request, 'workers/workers_profile.html', {'workers': workers})

    def post(self, request):
        worker_instance = get_object_or_404(User, id=int(request.POST['worker']))
        garage_instance = get_object_or_404(Garage, id=int(request.POST['garage']))
        data = {
            'worker': worker_instance,
            'garage': garage_instance,
            'experience': request.POST['experience'],
            'expertise': request.POST['expertise'],
            'is_verified': request.POST.get('is_verified', False),
            'is_active': request.POST.get('is_active', True),
        }
        create_worker(data)
        return redirect('workers')

class WorkerUpdate(View):
    def get(self, request, worker_id):
        worker = get_worker_by_id(worker_id)
        # if worker is None:
        #     return redirect('workers')  # Redirect if worker does not exist
        return render(request, 'workers/workers_profile_update.html', {'worker': worker})

    def post(self, request, worker_id):
        worker_instance = get_object_or_404(User, id=int(request.POST['worker']))
        garage_instance = get_object_or_404(Garage, id=int(request.POST['garage']))
        data = {
            'worker': worker_instance,
            'garage': garage_instance,
            'experience': request.POST['experience'],
            'expertise': request.POST['expertise'],
            'is_verified': request.POST.get('is_verified', False),
            'is_active': request.POST.get('is_active', True),
        }
        # if update_worker(worker_id, data) is None:
        #     return redirect('workers')  # Redirect if worker does not exist
        # return redirect('workers')
        return render(request, 'workers/workers_profile_update.html',data)

class WorkerDelete(View):
    def get(self, request, worker_id):
        worker = get_worker_by_id(worker_id)
        # if worker is None:
        #     return redirect('workers')  # Redirect if worker does not exist
        return render(request, 'workers/workers_profile_delete.html', {'worker': worker})

    def post(self, request, worker_id):
        # if not delete_worker(worker_id):
        #     return redirect('workers')  # Redirect if worker does not exist
        # return redirect('workers')
        return render(request, 'workers/workers_profile_delete.html')