from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service,booking_service
from django.shortcuts import render
from ..decorators import auth_required, role_required, garage_required, worker_required
from ..constants import Role,PayType

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
# @garage_required
# @worker_required
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
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentCreateView(View):
    def get(self, request,booking_id):
        booking_id=booking_id
        services=booking_service.get_services_by_id(booking_id)
        total_price=booking_service.total_price(services)
        payment = payment_service.get_current_payment(booking_id)
        return render(request, 'enduser/payment/payment.html', {"payment": payment,'booking_id':booking_id,'total_price':total_price})

    """Create a payment"""
    def post(self, request, booking_id):
        print("actual payment :  ", request.user.id)
        user_id = request.user.id
        booking = booking_service.get_booking_by_id(request.user.id)
        print("booking:", booking)

        if not booking:
            return JsonResponse({"error": "❌ No booking found for user"}, status=400)

        # ✅ Fix: Directly return response instead of wrapping it again
        return payment_service.create_payment(request, booking.id, user_id)  


auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentReceipt(View):
    def get(self,request,payment_id):
        payment=payment_service.payment_details_by_payment_id(payment_id)
        if payment['type'] == PayType.CASH.value:
            booking = booking_service.get_booking(payment['booking_id'])
            if booking and booking.assigned_worker:
                paid_to = f"{booking.assigned_worker.worker.first_name} {booking.assigned_worker.worker.last_name}".strip()
            else:
                paid_to = "Unknown"
            type="CASH"
        else:
            paid_to = "Quick-come Company"
            type="UPI"
        payment["paid_to"]=paid_to
        payment["type"]=type
        print(payment)
        return render(request, 'enduser/payment/reciept.html',{'payment':payment})
