from qcome.models import Worker
from django.core.exceptions import ObjectDoesNotExist

def get_all_workers():
    return Worker.objects.all()

def get_worker_by_id(worker_id):
    try:
        return Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return None

def create_worker(data):
    worker = Worker(**data)
    worker.save()
    return worker

def update_worker(worker_id, data):
    try:
        worker = Worker.objects.get(id=worker_id)
        for field, value in data.items():
            setattr(worker, field, value)
        worker.save()
        return worker
    except Worker.DoesNotExist:
        return None

def delete_worker(worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
        worker.delete()
        return True
    except Worker.DoesNotExist:
        return False
