from ..models import Worker,User,Garage
from qcome.package.file_management import save_uploaded_file

def get_worker_details(worker_id):
    try:
        return Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return None

def worker_create(user, expertise, experience, worker_garage):
    return Worker.objects.create(
        worker = user,
        garage = worker_garage,
        experience = experience,
        expertise = expertise
    )


def worker_update(worker, expertise, experience, worker_garage, user):
    if worker:
        worker.experience = experience
        worker.expertise = expertise
        worker.garage = worker_garage
        worker.updated_by = user
        worker.save()
        return worker
    return None


def update_worker_details(worker_id, worker_name, worker_phone, experience, expertise, garage_id, user_id, profile_picture):
    try:
        worker = Worker.objects.get(id=worker_id)
        user = User.objects.get(id=user_id)
        name_parts = worker_name.split()  # Split the name into components (First, Middle, Last)
        user.first_name = name_parts[0] if len(name_parts) > 0 else user.first_name
        user.last_name = name_parts[-1] if len(name_parts) > 1 else user.last_name
        user.middle_name = ' '.join(name_parts[1:-1]) if len(name_parts) > 2 else ""
        user.phone = worker_phone
        if profile_picture:
            user.profile_photo_url = profile_picture
        user.save()

        worker.experience = experience
        worker.expertise = expertise
        worker.garage_id = garage_id
        worker.save()

    except Worker.DoesNotExist:
        print(f"Worker with ID {worker_id} does not exist.")
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")

def handle_profile_photo(user_id, profile_picture):
    user = User.objects.get(id=user_id)
    profile_photo_path = user.profile_photo_url  
    if profile_picture:
        profile_photo_path = save_uploaded_file(profile_picture, subfolder='profile-images')
        user.profile_photo_url = profile_photo_path
        user.save() 

    return profile_photo_path

def is_user_a_garage_worker(user):
    return Worker.objects.filter(worker=user, is_active=True).exists()

def get_worker_of_garage(garage_id):
    return list(Worker.objects.filter(garage=garage_id, is_active=True))

def get_worker_object(worker_id):
    return Worker.objects.get(id=worker_id)

def get_all_workers():
    return Worker.objects.all()

def worker_toggle(worker_id):
    worker = get_worker_details(worker_id)

    if worker:
        worker.is_active = not worker.is_active
        worker.save()
        return worker
    
    return None

def get_worker_id(user):
    return Worker.objects.filter(worker=user).first()

def get_check(user):
    return Worker.objects.filter(worker=user).exists()


