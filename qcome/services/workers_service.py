from ..models import Worker

def worker_create(user, expertise, experience, worker_garage):
    return Worker.objects.create(
        worker = user,
        garage = worker_garage,
        experience = experience,
        expertise = expertise
    )


def get_worker_details(worker_id):
    try:
        return Worker.objects.get(id=worker_id) 
    except Worker.DoesNotExist:
        return None


def is_user_a_garage_worker(user):
    return Worker.objects.filter(worker=user, is_active=True).exists()