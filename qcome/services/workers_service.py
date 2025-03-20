from ..models import Worker

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


def update_worker_details(worker_id, worker_name, worker_phone, experience, expertise, garage_id):
    try:
        worker = Worker.objects.get(id=worker_id)
        worker.name = worker_name
        worker.phone = worker_phone
        worker.experience = experience
        worker.expertise = expertise
        worker.garage_id = garage_id  
        worker.save()
    except Worker.DoesNotExist:
        print(f"Worker with ID {worker_id} does not exist.")


def is_user_a_garage_worker(user):
    return Worker.objects.filter(worker=user, is_active=True).exists()

def get_worker_of_garage(garage_id):
    return list(Worker.objects.filter(garage=garage_id, is_active=True))

def get_worker_object(worker_id):
    return Worker.objects.get(id=worker_id)

def get_worker_id(user):
    return Worker.objects.get(worker=user)