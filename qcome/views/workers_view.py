import json
from django.views import View
from django.shortcuts import render,redirect
from ..services import user_service, garage_service, workers_service, payment_service,booking_service,work_service
from django.http import JsonResponse
from django.contrib import messages
from ..constants.success_message import SuccessMessage
from ..constants.error_message import ErrorMessage
from ..decorators import auth_required, garage_required,worker_required



@auth_required(login_url='/sign-in/')
@worker_required
class WorkerView(View):
    def get(self,request):
        user_id = request.user.id
        worker_id=workers_service.get_worker_id(user_id)
        worker_details = workers_service.get_worker_details(worker_id.id)
        garage_details = user_service.get_all_garages()
        context = {
            'worker_details':worker_details,
            'gargae_details':garage_details,
            'user':request.user,
            }
        return render(request,'worker/workers_profile.html',context)    


@auth_required(login_url='/sign-in/')
class WorkerCreateView(View):
    def get(self, request, worker_id):
        worker_details = workers_service.get_worker_details(worker_id)
        garage_details = user_service.get_all_garages()

        context = {
            'worker_details': worker_details,
            'user': request.user,
            'garage_details': garage_details,
        }
        return render(request, 'enduser/profile/garage_worker/worker_profile_create.html', context)

    def post(self, request, worker_id):
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        worker_garage = request.POST.get('garage')

        # Validate essential fields
        if not all([worker_id, worker_phone, experience, expertise, worker_garage]):
            messages.error(request, "All fields are required.")
            return redirect('worker', worker_id=worker_id)

        user = user_service.get_user(worker_id)

        if not user:
            messages.error(request, "User not found.")
            return redirect('worker', worker_id=worker_id)

        is_worker = workers_service.is_user_a_garage_worker(user)

        if not is_worker:
            garage = garage_service.get_garage(worker_garage)
            if not garage:
                messages.error(request, "Garage not found.")
                return redirect('worker', worker_id=worker_id)

            workers_service.worker_create(user, expertise, experience, garage)
            user_service.user_phone_create(user, worker_phone)
            messages.success(request, SuccessMessage.S00022.value)
        else:
            messages.error(request, ErrorMessage.E00017.value)


@auth_required(login_url='/sign-in/')
@worker_required
class WorkerUpdateView(View):
    def get(self, request, worker_id):
        worker_details = workers_service.get_worker_details(worker_id)
        garage_details = user_service.get_all_garages()
        context = {
            'worker_details': worker_details,
            'gargae_details': garage_details,
            'user': request.user,
        }
        return render(request, 'worker\worker_profile_update.html', context)
    
    def post(self, request, worker_id):
        worker_name = request.POST.get('worker_name')
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        garage_id = request.POST.get('garage')
        
        workers_service.update_worker_details(worker_id, worker_name, worker_phone, experience, expertise, garage_id)
        messages.success(request,SuccessMessage.S00023.value)
        return redirect('worker',worker_id = worker_id)  

@auth_required(login_url='/sign-in/')
@worker_required
class WorkerDeleteView(View):
    def post(self, request, worker_id):
        worker = workers_service.get_worker_details(worker_id)
        if worker:
            worker.delete()
        messages.success(request,SuccessMessage.S00024.value)
        return redirect('home')
  

@auth_required(login_url='/sign-in/')
@worker_required
class WorkerPaymentListView(View):
    def get(self, request):
        worker_user_id = request.user.id
        payments = payment_service.get_worker_payments(worker_user_id)

        # Convert Decimal to string for safe rendering
        for payment in payments:
            payment["amount"] = str(payment["amount"])

        print("Payments Data:", payments)  # Debugging

        return render(request, "worker/worker_payment_list.html", {"payments": payments})
    

    
@auth_required(login_url='/sign-in/')
class CheckWorkerStatus(View):
    def get(self, request):
        user_id = request.user.id
        is_worker = workers_service.is_user_a_garage_worker(user_id)
        
        return JsonResponse({"is_worker": is_worker})
    

    
@auth_required(login_url='/sign-in/')
@garage_required 
class AssignedWorkerCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            worker_id = data.get('worker_id')
            booking_id = data.get('booking_id')

            if not worker_id or not booking_id:
                return JsonResponse({'message': 'Invalid data provided', 'status': 'error'}, status=400)

            booking = booking_service.get_booking_object(booking_id)
            worker = workers_service.get_worker_object(worker_id)

            if not booking or not worker:
                return JsonResponse({'message': 'Invalid worker or booking', 'status': 'error'}, status=404)

            booking.assigned_worker = worker
            booking.save()

            work_service.work_create(booking,booking.assigned_worker,booking.customer)
            return JsonResponse({'message': 'Worker assigned successfully', 'status': 'success'})
        
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)
        
        
    
@auth_required(login_url='/sign-in/')
@worker_required
class WorkerWorkRecieptView(View):
    def get(self, request, work_id):
        try:
            print("work_id ", work_id)
            # Fetch work details using the work_id
            work = work_service.get_work_by_id(work_id)
            is_updatable=work_service.is_work_status_updatable(work_id)
            # Fetch status options (e.g., 4, 5, 6)
            statuss = work_service.get_statuss_work_id()

            if not work:
                return JsonResponse({'message': 'Work not found', 'status': 'error'}, status=404)

            # Pass work data and status options to the template
            return render(request, 'worker/work/work_details.html', {'work_data': work, 'statuss': statuss, 'is_changable':is_updatable})
        
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)

    def post(self, request, work_id):  # Include work_id here
        try:
            data = json.loads(request.body)
            print(data)
            work_id = data.get('work_id')
            status = data.get('status')
            
            if not work_id or not status:
                return JsonResponse({'message': 'Invalid data provided', 'status': 'error'}, status=400)

            work = work_service.get_work_by_id(work_id)
            if not work:
                return JsonResponse({'message': 'Work not found', 'status': 'error'}, status=404)

            # Update work status
            work_service.update_work_status(work_id, status)
            
            return JsonResponse({'message': 'Status updated successfully', 'status': 'success', 'updated_status': status})
        
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)