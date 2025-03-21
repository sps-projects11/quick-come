import json
from django.views import View
from django.shortcuts import render,redirect
from ..services import user_service, garage_service, workers_service, payment_service,booking_service,work_service
from ..models import Worker
from django.http import JsonResponse


class WorkerCreateView(View):
    def get(self, request,worker_id):
        worker_details = user_service.get_workers_details(worker_id)
        garage_details = user_service.get_all_garages() 
        context = {
            'worker_details': worker_details,
            'user': request.user,
            'garage_details':garage_details,
        }
        return render(request, 'enduser/profile/garage_worker/worker_profile_create.html', context)

    def post(self, request, worker_id):
        worker_id = request.POST.get('worker_id')
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        worker_garage = request.POST.get('garage')

        user = user_service.get_user(worker_id)
        garage = garage_service.get_garage(worker_garage)
        
        workers_service.worker_create(user, expertise, experience, garage)
        user_service.user_phone_create(user, worker_phone)

        return redirect('home')

    
class WorkerUpdateView(View):
    def get(self, request, worker_id):
        worker_details = workers_service.get_worker_details(worker_id)
        context = {'worker_details': worker_details}
        return render(request, 'workers/worker_profile_update.html', context)

    def post(self, request, worker_id):
        worker = workers_service.get_worker_details(worker_id)
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
    

class WorkerPaymentListView(View):
    def get(self, request):
        worker_user_id = request.user.id
        payments = payment_service.get_worker_payments(worker_user_id)

        # Convert Decimal to string for safe rendering
        for payment in payments:
            payment["amount"] = str(payment["amount"])

        print("Payments Data:", payments)  # Debugging

        return render(request, "worker/worker_payment_list.html", {"payments": payments})
    
    
class CheckWorkerStatus(View):
    def get(self, request):
        user_id = request.user.id
        is_worker = workers_service.is_user_a_garage_worker(user_id)
        
        return JsonResponse({"is_worker": is_worker})
    

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
    

class WorkerWorkRecieptView(View):
    def get(self,request,work_id):
        print("work_id ",work_id)
        work = work_service.get_work_by_id(work_id)
        return render(request,'worker/work/work_details.html',{'work_data':work})