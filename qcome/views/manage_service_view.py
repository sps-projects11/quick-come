from django.views import View
from django.shortcuts import render, redirect
from ..services import service_service 
from ..constants import Role
import os
import hashlib
from django.conf import settings
from django.http import HttpResponse

class ManageServiceList(View):
    def get(self, request):
        service = service_service.service_List()
        return render(request, 'adminuser/service_catalog/service_catalog.html',{'services':service})
    

class ManageServiceListCreate(View):
    def get(self, request):
        return render(request, 'adminuser/service_catalog/service_catalog_from.html')
    
    def post(self, request):
        user = request.user
        if user.roles in (Role.ADMIN.value, Role.SUPER_ADMIN.value):
            service_name = request.POST.get('service_name', '')
            spare_part = request.POST.get('spare_part', '')
            price = request.POST.get('price', '')
            
            service_image_file = request.FILES.get('service_image')
            service_image_path = ''  # Default to empty if no file is provided
            
            if service_image_file:
                # Define the static directory path where you want to save the image
                static_upload_dir = os.path.join(settings.BASE_DIR, 'static', 'all-Pictures', 'uploads')
                # Create the directory if it doesn't exist
                if not os.path.exists(static_upload_dir):
                    os.makedirs(static_upload_dir)
                
                # Compute a hash of the file's content
                md5_hash = hashlib.md5()
                for chunk in service_image_file.chunks():
                    md5_hash.update(chunk)
                file_hash = md5_hash.hexdigest()
                
                # Get the original file extension (e.g. .jpg, .png)
                _, ext = os.path.splitext(service_image_file.name)
                new_file_name = f"{file_hash}{ext}"
                file_path = os.path.join(static_upload_dir, new_file_name)
                
                # Check if a file with this hash already exists
                if not os.path.exists(file_path):
                    # Rewind the file pointer since we've read the file for hashing
                    service_image_file.seek(0)
                    # Save the file in chunks
                    with open(file_path, 'wb+') as destination:
                        for chunk in service_image_file.chunks():
                            destination.write(chunk)
                
                # Set the URL for the saved image (using static URL)
                service_image_path = f'/static/all-Pictures/uploads/{new_file_name}'
            
            # Save the service record using your service_create helper function
            service_service.service_create(user, service_name, service_image_path, spare_part, price)
            return redirect('manage_service_list')
        else:
            return HttpResponse("Unauthorized", status=403)



class ManageServiceListUpdate(View):
    def get(self, request, service_id):
        return


class ManageServiceListDelete(View):
    def post(self, request, service_id):
        return
    
        