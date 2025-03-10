from django.http import JsonResponse
from django.views import View
from qcome.services import payment_service
from django.shortcuts import render

class PaymentListView(View):
    """Retrieve all payments"""
    def get(self, request):
        user_id = request.user.id
        payments = payment_service.get_all_payments(user_id)
        return render(request, 'enduser/payment/payment.html', {"payments": payments})



class PaymentCreateView(View):
    """Create a payment"""
    def post(self, request, booking_id):
        response = payment_service.create_payment(request, booking_id)
        return JsonResponse(response)


class PaymentUpdateView(View):
    """Update an existing payment"""
    def post(self, request, booking_id):
        response = payment_service.update_payment(request, booking_id)
        return JsonResponse(response)


class PaymentDeleteView(View):
    """Delete a payment"""
    def post(self, request, booking_id):
        response = payment_service.delete_payment(booking_id)
        return JsonResponse(response)
