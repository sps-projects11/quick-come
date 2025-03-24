from django.views import View
from django.shortcuts import render
from qcome.services import payment_service, user_service
from qcome.constants import Role
from qcome.decorators import auth_required, role_required



@auth_required(login_url='/login/admin/')
@role_required(Role.ADMIN.value, Role.SUPER_ADMIN.value, page_type='admin')
class ManagePaymentListView(View):
    def get(self, request):
        admin_data = user_service.get_user(request.user.id)
        payments = payment_service.get_all_payments()
        return render(request, 'adminuser/payments/payment_list.html', { 'payments_data': payments, 'admin': admin_data})
    

