from django.views import View
from django.shortcuts import render, redirect
from qcome.services import garage_service, user_service, workers_service
from django.http import JsonResponse
from django.contrib import messages 
from ..constants.error_message import ErrorMessage
from ..constants.success_message import SuccessMessage
from ..package.response import success_response,error_response
from qcome.package.file_management import save_uploaded_file
from qcome.constants.default_values import Role
from qcome.decorators import auth_required, role_required


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
class ManageWorkerListView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
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
        return render(request, 'adminuser/worker/worker_list.html', {'workers': workers, 'admin': admin_data})        
    


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
class ManageWorkerCreateView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        available_worker = user_service.get_non_garage_and_non_worker_users()
        all_garage = user_service.get_all_garages()
        return render(request, 'adminuser/worker/worker_create.html', {'all_garage': all_garage, 'available_worker': available_worker, 'admin': admin_data})
    
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
            user_service.user_phone_create(worker, worker_phone)
            user_service.user_profile_photo_create(worker, worker_profile_photo_path)
            messages.success(request, SuccessMessage.S00009.value)
            return redirect('manage_worker_list')
        except Exception as e:
            print("Error occurred:", e)
            messages.error(request, ErrorMessage.E00017.value)
            return redirect('manage_worker_create')
    


@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
class ManageWorkerUpdateView(View):
    def get(self, request, worker_id):
        admin_data = user_service.get_user(request.user.id)
        worker = workers_service.get_worker_details(worker_id)
        worker_user = user_service.get_user(worker.worker.id)
        worker.worker_first_name = worker_user.first_name
        worker.worker_middle_name = worker_user.middle_name
        worker.worker_last_name = worker_user.last_name
        worker.worker_image = worker_user.profile_photo_url
        worker.phone = worker_user.phone
        worker_garage = garage_service.get_garage(worker.garage.id)
        worker.garage_name = worker_garage.garage_name

        all_garage = garage_service.get_all_garages_exclude_worker_garage(worker.garage.id)

        return render(request, 'adminuser/worker/worker_update.html', {'worker': worker, 'all_garage':all_garage, 'admin': admin_data})
    
    def post(self, request, worker_id):
        worker_first_name = request.POST.get('worker_first_name')
        worker_middle_name = request.POST.get('worker_middle_name', '')
        worker_last_name = request.POST.get('worker_last_name')
        garage = request.POST.get('worker_garage')
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        worker_profile_photo = request.FILES.get('worker_profile_photo')

        worker_profile_photo_path = save_uploaded_file(worker_profile_photo, 'worker-profile-photo')

        worker = workers_service.get_worker_details(worker_id)
        worker_user = user_service.get_user(worker.worker.id)
        worker_garage = garage_service.get_garage(garage)
        try:
            workers_service.worker_update(worker, expertise, experience, worker_garage, request.user)
            user_service.user_name_update(worker_user, worker_first_name, worker_middle_name, worker_last_name)
            user_service.user_phone_create(worker_user, worker_phone)
            user_service.user_profile_photo_create(worker_user, worker_profile_photo_path)
            messages.success(request, SuccessMessage.S00009.value)
            return redirect('manage_worker_list')
        except Exception as e:
            print("Error occurred:", e)
            messages.error(request, ErrorMessage.E00017.value)
            return redirect('manage_worker_list')



@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value,  page_type='admin')
class ManageWorkerToggleView(View):
    def post(self, request, worker_id):
        worker = workers_service.worker_toggle(worker_id)
        if worker is None:
            return JsonResponse(error_response(ErrorMessage.E00018.value))
                
        return JsonResponse(success_response(SuccessMessage.S00010.value))