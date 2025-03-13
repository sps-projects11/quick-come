from django.shortcuts import render
from django.views import View

# class GarageHomeView(View):
#     def get(self, request):
#         navbar_labels = {
#             "home": "Garage Home",
#             "booking": "Garage Bookings",
#             "contact": "Garage Worker",
#             "blog": "Payment",
#         }

#         navbar_urls = {
#             "home": "/garage/",
#             "booking": "/garage/booking/",
#             "contact": "/garage/workers/",
#             "blog": "/garage/payment/",
#         }

#         return render(request, 'garage/index.html', {
#             'navbar_labels': navbar_labels,
#             'navbar_urls': navbar_urls,
#             'is_garage_page': True  # Flag to check if it's a garage page
#         })




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

             
