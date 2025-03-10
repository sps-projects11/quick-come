from django.views import View

class GarageListView(View):
    def get(self, request):
        return 

class GarageCreateView(View):
    def get(self, request):
        return
    def post(self, request):
        return

class GarageUpdateView(View):
    def get(self, request, garage_id):
        return
    def post(self, request, garage_id):
        return

class GarageDeleteView(View):
    def get(self, request, garage_id):
        return
    def post(self, request, garage_id):
        return

             
