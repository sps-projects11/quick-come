from django.shortcuts import render, redirect
from django.views import View
from ..services import get_all_workers, get_worker_by_id, create_worker, update_worker, delete_worker

class Worker(View):
    def get(self, request):
        workers = get_all_workers()
        return render(request, 'workers/workers_profile.html', {'workers': workers})

    def post(self, request):
        data = {
            'worker': request.POST['worker'],
            'garage': request.POST['garage'],
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
        if worker is None:
            return redirect('worker_list')  # Redirect if worker does not exist
        return render(request, 'workers/workers_profile_update.html', {'worker': worker})

    def post(self, request, worker_id):
        data = {
            'worker': request.POST['worker'],
            'garage': request.POST['garage'],
            'experience': request.POST['experience'],
            'expertise': request.POST['expertise'],
            'is_verified': request.POST.get('is_verified', False),
            'is_active': request.POST.get('is_active', True),
        }
        if update_worker(worker_id, data) is None:
            return redirect('worker_list')  # Redirect if worker does not exist
        return redirect('workers')

class WorkerDelete(View):
    def get(self, request, worker_id):
        worker = get_worker_by_id(worker_id)
        if worker is None:
            return redirect('worker_list')  # Redirect if worker does not exist
        return render(request, 'workers/workers_profile_delete.html', {'worker': worker})

    def post(self, request, worker_id):
        if not delete_worker(worker_id):
            return redirect('worker_list')  # Redirect if worker does not exist
        return redirect('workers')
