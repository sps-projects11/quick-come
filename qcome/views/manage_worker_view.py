from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service, workers_service
from django.http import JsonResponse
from django.contrib import messages 
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from qcome.package.file_management import save_uploaded_file


class ManageWorkerListView(View):
    def get(self, request):
        workers = workers_service.get_all_workers()
        for worker in workers:
            worker_user_id = user_service.get_user(worker.worker.id)
            worker.worker_name = (
                f"{worker_user_id.first_name} "
                f"{(worker_user_id.middle_name + ' ') if worker_user_id.middle_name else ''}"
                f"{worker_user_id.last_name}"
            )
            worker.worker_image = worker_user_id.profile_photo_url
            worker.phone = worker_user_id.phone
            worker_garage = garage_service.get_garage(worker.garage.id)
            worker.garage_name = worker_garage.garage_name
        return render(request, 'adminuser/worker/worker_list.html', {'workers': workers})        
    

class ManageWorkerCreateView(View):
    def get(self, request):
        available_worker = user_service.get_non_garage_and_non_worker_users()
        all_garage = garage_service.get_all_garages()
        return render(request, 'adminuser/worker/worker_create.html', {'all_garage': all_garage, 'available_worker': available_worker})
    
    def post(self, request):
        worker_user = request.POST.get('worker_user')
        garage = request.POST.get('worker_garage')
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        worker_profile_photo = request.FILES.get('worker_profile_photo')

        worker_profile_photo_path = save_uploaded_file(worker_profile_photo, 'worker-profile-photo') 


        worker = user_service.get_user(worker_user)
        worker_garage = garage_service.get_garage(garage)

        try:
            workers_service.worker_create(worker, expertise, experience, worker_garage)
            messages.success(request, SuccessMessage.S00009.value)
            return redirect('manage_worker_list')
        except Exception as e:
            print("Error occurred:", e)
            messages.error(request, ErrorMessage.E00017.value)
            return redirect('manage_worker_create')
    

class ManageWorkerUpdateView(View):
    def get(self, request, worker_id):
        return render(request, 'adminuser/worker/worker_update.html.html')
    
    def post(self, request, worker_id):
        return redirect('manage_worker_list')


class ManageWorkerToggleView(View):
    def post(self, request, worker_id):
        return redirect('manage_worker_list')