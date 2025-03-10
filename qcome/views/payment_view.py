from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service,booking_service
from django.shortcuts import render
from ..decorators import auth_required, role_required
from ..constants import Role

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentListView(View):
    """Retrieve all payments"""
    def get(self, request):
        user_id = request.user.id
        payments = payment_service.get_all_payments(user_id)
        return render(request, 'enduser/payment/payment.html', {"payments": payments})


@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentCreateView(View):
    """Create a payment"""
    def post(self, request, booking_id):
        booking = booking_service.get_booking_id(request.user.id)
        print("booking:", booking)
        if not booking:
            return JsonResponse({"error": "❌ No booking found for user"}, status=400)

        response = payment_service.create_payment(request, booking.id)
        return JsonResponse(response) 

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentUpdateView(View):
    """Update an existing payment"""
    def post(self, request, booking_id):
        response = payment_service.update_payment(request, booking_id)
        return JsonResponse(response)

@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentDeleteView(View):
    """Delete a payment"""
    def post(self, request, booking_id):
        response = payment_service.delete_payment(booking_id)
        return JsonResponse(response)
@auth_required(login_url='/sign-in/')
@role_required(Role.END_USER.value, page_type='enduser')
class PaymentReceipt(View):
    def get(self,request):
        return render(request, 'enduser/payment/reciept.html')
