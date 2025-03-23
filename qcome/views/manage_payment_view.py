from django.views import View
from django.shortcuts import render
from qcome.services import payment_service, user_service


class ManagePaymentListView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        payments = payment_service.get_all_payments()
        return render(request, 'adminuser/payments/payment_list.html', { 'payments_data': payments, 'admin': admin_data})
    

