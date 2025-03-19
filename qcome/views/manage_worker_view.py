from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service, workers_service
from django.http import JsonResponse
from django.contrib import messages 
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
import os
import hashlib
from quickcome import settings


class ManageWorkerListView(View):
    def get(self, request):
        workers = workers_service.get_all_workers()
        for worker in workers:
            worker_user_id = user_service.get_user(worker.worker_id)
            worker.name = (
                f"{worker.first_name} "
                f"{(worker.middle_name + ' ') if worker.middle_name else ''}"
                f"{worker.last_name}"
            )
            worker.image = worker_user_id.profile_photo_url
            worker.phone = worker_user_id.phone
            worker_garage = garage_service.get_garage(worker.garage_id)
            worker.garage = worker_garage.name
        print(workers)
        return render(request, 'adminuser/worker/worker_list.html', {'workers': workers})        
    

class ManageWorkerCreateView(View):
    def get(self, request):
        return render(request, 'adminuser/worker/worker_create.html')
    
    def post(self, request):
        return redirect('manage_worker_list')
    

class ManageWorkerUpdateView(View):
    def get(self, request, worker_id):
        return render(request, 'adminuser/worker/worker_update.html.html')
    
    def post(self, request, worker_id):
        return redirect('manage_worker_list')


class ManageWorkerToggleView(View):
    def post(self, request, worker_id):
        return redirect('manage_worker_list')