import json
from django.views import View
from django.shortcuts import render,redirect
from ..services import user_service, garage_service, workers_service, payment_service,booking_service,work_service
from django.http import JsonResponse
from django.contrib import messages
from ..constants.success_message import SuccessMessage
from ..constants.error_message import ErrorMessage
from ..decorators import auth_required, garage_required,worker_required
from ..models import User
from qcome.package.file_management import save_uploaded_file
from qcome.constants.default_values import Vehicle_Type,Status,PayStatus

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
    def get(self, request):  
        garage_details = user_service.get_all_garages()

        context = {
            'user': request.user,
            'garage_details': garage_details,
        }
        return render(request, 'enduser/profile/garage_worker/worker_profile_create.html', context)

    def post(self, request):
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        garage = request.POST.get('garage')
        worker_worker_id = request.POST.get('user_id')
        is_exists=workers_service.is_user_a_garage_worker(worker_worker_id)
        if is_exists:
            return redirect('worker')
        worker_instance = user_service.get_user(worker_worker_id)
        worker_garage = garage_service.get_garage(garage)
        worker = workers_service.worker_create(worker_instance, expertise, experience, worker_garage)
        
        worker_phone=user_service.user_phone_create(worker_instance,worker_phone)
        if worker:
            return redirect('worker')
        

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
        return render(request, 'worker/worker_profile_update.html', context)
    
    def post(self, request, worker_id):
        user_id = request.user.id
        worker_name = request.POST.get('worker_name')
        worker_phone = request.POST.get('worker_phone')
        experience = request.POST.get('experience')
        expertise = request.POST.get('expertise')
        garage_id = request.POST.get('garage')
        profile_picture = request.FILES.get('profile_picture')
        profile_photo_path = user_service.get_user_profile_photo(user_id) 
        if profile_picture:
            profile_photo_path = save_uploaded_file(profile_picture, subfolder="profile-images")
            print("Updated profile photo path:", profile_photo_path)
        else:
            profile_photo_path = "/static/all-Pictures/user.jpg"
        # ✅ Make a mutable copy of request.POST
        mutable_post = request.POST.copy() # Add new profile photo path
        mutable_post['profile_photo_url'] = profile_photo_path # Pass the modified request data
        workers_service.update_worker_details(worker_id, worker_name, worker_phone, experience, expertise, garage_id, user_id, profile_photo_path)
        messages.success(request, SuccessMessage.S00023.value)
        return redirect('worker')


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

            work_service.work_create(booking, booking.assigned_worker, booking.customer)
            work_id=work_service.get_work_id(booking_id)
            # Emit WebSocket event
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "worker_updates",
                {
                    "type": "send_worker_update",
                    "data": {
                        "message": "Worker assigned to booking",
                        "booking_id": booking.id,
                        "customer_name": f"{booking.customer.first_name} {booking.customer.last_name}",
                        "vehicle_type":Vehicle_Type(booking.vehicle_type).name,
                        "location":booking.current_location,
                        "services":booking_service.get_booking_service(booking.service),
                        "work_id":work_id,
                        "status":Status(booking_service.get_booking_status(booking.id)).name,
                    },
                },
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "booking_updates",  # Group name
                {
                    "type": "send_booking_update",
                    "message": "Booking status updated",
                    "booking_id": booking.id,  # Updated key to booking_id
                    "new_status": Status(booking_service.get_booking_status(booking.id)).name,  # Ensure status is sent
                }
            )

            return JsonResponse({'message': 'Worker assigned successfully', 'status': 'success'})

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)

        
    
@auth_required(login_url='/sign-in/')
class WorkerWorkRecieptView(View):
    def get(self, request, work_id):
        work = work_service.get_work_by_id(work_id)
        print("work:",work)
        is_updatable = work_service.is_work_status_updatable(work_id)
        statuss = work_service.get_statuss_work_id()

        if not work:
            return redirect('worker')
        return render(request, 'worker/work/work_details.html', {'work_data': work, 'statuss': statuss, 'is_changable': is_updatable})

    def post(self, request, work_id):
        try:
            data = json.loads(request.body)
            work_id = data.get('work_id')
            status = data.get('status')
            if not work_id or not status:
                return JsonResponse({'message': 'Invalid data provided', 'status': 'error'}, status=400)

            work = work_service.get_work_by_id(work_id)
            if not work:
                return JsonResponse({'message': 'Work not found', 'status': 'error'}, status=404)
            booking_service.update_booking_status(work_id,status)
            # Update work status
            work_service.update_work_status(work_id, status)
            booking=booking_service.get_booking_id(work_id)
            status_value=booking_service.get_booking_status(booking.id)
            status_name=booking_service.get_status_name(status_value)
            if status_value == Status.COMPLETED.value:
                channel_layer = get_channel_layer()
                # Convert datetime to ISO format string
                created_at_str = booking.created_at.isoformat()
                # Get the total price from the service (assuming this returns a Decimal)
                total_price = booking_service.get_service_price(booking.id)
                # Convert Decimal to float before serializing
                total_price_float = float(total_price)

                async_to_sync(channel_layer.group_send)(
                    "garage_bills",
                    {
                        "type": "bill_create",
                        "bill": json.dumps({
                            "message": "✅ Work completed successfully",
                            "booking_id": booking.id,
                            "vehicle_type": Vehicle_Type(booking.vehicle_type).name,
                            "created_at": created_at_str,
                            "total": total_price_float,  # Ensure it's a float for JSON serialization
                            "pay_status":PayStatus.NOT_PAID.name,
                        }),
                    }
                )
            # **Trigger WebSocket Event**
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "booking_updates",  # Group name
                {
                    "type": "send_booking_update",
                    "message": "Booking status updated",
                    "booking_id": booking.id,  # Updated key to booking_id
                    "new_status": status_name,  # Ensure status is sent
                }
            )

            return JsonResponse({'message': 'Status updated successfully', 'status': 'success', 'updated_status': status})

        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}', 'status': 'error'}, status=500)