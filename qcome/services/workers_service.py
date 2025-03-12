from ..models import Worker

def get_worker_details(worker_id):
    try:
        return Worker.objects.get(id=worker_id) 
    except Worker.DoesNotExist:
        return None
