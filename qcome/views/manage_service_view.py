from django.views import View


class ManageServiceList(View):
    def get(self, request):
        return
    

class ManageServiceListCreate(View):
    def get(self, request):
        return
    
    def post(self, request):
        return

class ManageServiceListUpdate(View):
    def get(self, request, service_id):
        return


class ManageServiceListDelete(View):
    def post(self, request, service_id):
        return
    
        