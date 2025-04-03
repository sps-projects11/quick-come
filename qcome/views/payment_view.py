from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service, booking_service, workers_service, garage_service, user_service
from django.shortcuts import render,redirect
from ..decorators import auth_required, role_required, worker_required
from ..constants import Role,PayType,PayStatus

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentListView(View):
    """Retrieve all payments"""
    def get(self, request):
        user_id = request.user.id
        payments = payment_service.get_all_payments_created_by(user_id)  # Returns list of dicts

        payment_data = []
        for payment in payments:
            entry = {
                'user_id':user_id,
                'payment_id': payment['id'],
                'amount': payment['amount'],
                'type': PayType(payment['type']).name if payment['type'] else "N/A",
                'time': payment['paid_at'].strftime('%Y-%m-%d %H:%M:%S') if payment['paid_at'] else "N/A",
                'payment_by': user_service.user_full_name(payment.get('created_by')),
                'booking_id': payment['booking_id']
            }
            # Determine 'paid_to' field
            if payment['type'] == PayType.CASH.value:
                booking = booking_service.get_booking(payment['booking_id'])
                if booking and booking.assigned_worker:
                    entry['paid_to'] = user_service.user_full_name(booking.assigned_worker.worker)

                else:
                    entry['paid_to'] = "Unknown"
            else:
                entry['paid_to'] = "Quick-come Company"
            payment_data.append(entry)

        return render(request, 'enduser/payment/payment_list.html', {"payment_data": payment_data})


@auth_required(login_url='/sign-in/')
@worker_required
class PaymentCreateView(View):
    """Create a payment"""

    def get(self, request, booking_id):
        services = booking_service.get_services_by_id(booking_id)
        total_price = booking_service.total_price(services)
        payment = payment_service.get_current_payment(booking_id)
        return render(request, 'worker/payment.html', {"payment": payment, "booking_id": booking_id, "total_price": total_price})

    def post(self, request, booking_id):
        user_id = request.user.id
        return payment_service.create_payment(request, booking_id, user_id)  # 


@auth_required(login_url='/sign-in/')
class PaymentReceipt(View):
    def get(self,request,payment_id):
        payment=payment_service.payment_details_by_payment_id(payment_id)
        status =PayStatus(payment_service.get_payment_status(payment['booking_id'])).name
        if payment['type'] == PayType.CASH.value:
            booking = booking_service.get_booking(payment['booking_id'])
            if booking and booking.assigned_worker:
                paid_to = user_service.user_full_name(booking.assigned_worker.worker)
                paid_by = user_service.user_full_name(booking.customer)
            else:
                paid_to = "Unknown"
                paid_by = user_service.user_full_name(booking.customer)
            type="CASH"
        else:
            booking = booking_service.get_booking(payment['booking_id'])
            paid_to = "Quick-come Company"
            type="UPI"
            paid_by = user_service.user_full_name(booking.customer)
        payment["paid_to"]=paid_to
        payment["type"]=type
        payment["paid_by"]=paid_by
        payment["status"]=status
        worker=workers_service.is_user_a_garage_worker(request.user.id)
        is_garage = garage_service.is_user_a_garage_owner(request.user.id)
        if is_garage:
            return redirect('garage/profile/')
        if worker:
            return render(request, 'worker/reciept.html',{'payment':payment})
        return render(request, 'enduser/payment/reciept.html',{'payment':payment})
