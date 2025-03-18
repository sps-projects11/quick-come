from django.views import View
from django.shortcuts import render,redirect
from ..services import user_service, garage_service, workers_service, payment_service
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
        return render(request, 'worker/worker_profile_update.html', context)

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
        return render(request, 'worker/worker_profile_delete.html', context)

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

        return render(request, "enduser/payment/worker_payment_list.html", {"payments": payments})
    
    
class CheckWorkerStatus(View):
    def get(self, request):
        user_id = request.user.id
        is_worker = workers_service.is_user_a_garage_worker(user_id)
        
        return JsonResponse({"is_worker": is_worker})