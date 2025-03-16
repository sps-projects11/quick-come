from django.views import View
from django.shortcuts import render,redirect
from ..services import *
from ..models import Worker




    

    
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