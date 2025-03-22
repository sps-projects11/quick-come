from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service,booking_service,workers_service,garage_service
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
                'payment_id': payment['id'],
                'amount': payment['amount'],
                'type': PayType(payment['type']).name if payment['type'] else "N/A",
                'time': payment['paid_at'].strftime('%Y-%m-%d %H:%M:%S') if payment['paid_at'] else "N/A",
                'payment_by': f"{payment.get('created_by__first_name', 'Unknown')} {payment.get('created_by__last_name', '')}".strip(),
                'booking_id': payment['booking_id']
            }
            # Determine 'paid_to' field
            if payment['type'] == PayType.CASH.value:
                booking = booking_service.get_booking(payment['booking_id'])
                if booking and booking.assigned_worker:
                    entry['paid_to'] = f"{booking.assigned_worker.worker.first_name} {booking.assigned_worker.worker.last_name}".strip()
                else:
                    entry['paid_to'] = "Unknown"
            else:
                entry['paid_to'] = "Quick-come Company"
            payment_data.append(entry)

        return render(request, 'enduser/payment/payment_list.html', {"payment_data": payment_data})


@auth_required(login_url='/sign-in/')
@worker_required
class PaymentCreateView(View):
    def get(self, request,booking_id):
        booking_id=booking_id
        services=booking_service.get_services_by_id(booking_id)
        total_price=booking_service.total_price(services)
        payment = payment_service.get_current_payment(booking_id)
        return render(request, 'worker/payment.html', {"payment": payment,'booking_id':booking_id,'total_price':total_price})

    """Create a payment"""
    def post(self, request, booking_id):
        user_id = request.user.id
        booking = booking_service.get_booking_by_id(request.user.id)
        if not booking:
            return JsonResponse({"error": "❌ No booking found for user"}, status=400)

        # ✅ Fix: Directly return response instead of wrapping it again
        return payment_service.create_payment(request, booking.id, user_id)  


@auth_required(login_url='/sign-in/')
class PaymentReceipt(View):
    def get(self,request,payment_id):
        payment=payment_service.payment_details_by_payment_id(payment_id)
        status =PayStatus(payment_service.get_payment_status(payment['booking_id'])).name
        if payment['type'] == PayType.CASH.value:
            booking = booking_service.get_booking(payment['booking_id'])
            if booking and booking.assigned_worker:
                paid_to = f"{booking.assigned_worker.worker.first_name} {booking.assigned_worker.worker.last_name}".strip()
                paid_by = f"{booking.customer.first_name} {booking.customer.last_name}".strip()
            else:
                paid_to = "Unknown"
                paid_by = f"{booking.customer.first_name} {booking.customer.last_name}".strip()
            type="CASH"
        else:
            booking = booking_service.get_booking(payment['booking_id'])
            paid_to = "Quick-come Company"
            type="UPI"
            paid_by = f"{booking.customer.first_name} {booking.customer.last_name}".strip()
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
