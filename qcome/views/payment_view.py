from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service,booking_service
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role,PayType
from ..models import User

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentListView(View):
    """Retrieve all payments"""
    def get(self, request):
        user_id = request.user.id
        payments = payment_service.get_all_payments(user_id)  # Now returns dicts

        payment_data = [
                {
                'payment_id': payment['id'],
                'amount': payment['amount'],
                'type': PayType(payment['type']).name if payment['type'] else "N/A",
                'time': payment['paid_at'].strftime('%Y-%m-%d %H:%M:%S') if payment['paid_at'] else "N/A",
                'payment_by': f"{payment.get('created_by__first_name', 'Unknown')} {payment.get('created_by__last_name', '')}".strip()
                }
                for payment in payments
            ]
        return render(request, 'enduser/payment/payment_list.html', {"payment_data": payment_data})




@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentCreateView(View):
    def get(self, request,booking_id):
        booking=booking_id
        payment = payment_service.get_current_payment(booking_id)
        return render(request, 'enduser/payment/payment.html', {"payment": payment,'booking_id':booking_id})

    """Create a payment"""
    def post(self, request, booking_id):
        print("actual payment :  ",request.user.id)
        user_id=request.user.id
        booking = booking_service.get_booking_by_id(request.user.id)
        print("booking:", booking)
        if not booking:
            return JsonResponse({"error": "❌ No booking found for user"}, status=400)

        response = payment_service.create_payment(request, booking.id,user_id)
        return JsonResponse(response) 

auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentReceipt(View):
    def get(self,request,payment_id):
        payment=payment_service.payment_details_by_payment_id(payment_id)
        print(payment)
        return render(request, 'enduser/payment/reciept.html',{'payment':payment})
