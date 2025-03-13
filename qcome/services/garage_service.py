from ..models import Garage

def get_garage_list():
    garages = Garage.objects.all()
    return garages

def create_garage_list(garage_id):
    Garage.objects.create()
    return

def update_garage_list(garage_id):
    Garage.objects.update()
    return

def delete_garage_list(garage_id):
    Garage.objects.delete()
    return


def is_user_a_garage_owner(user):
    return Garage.objects.filter(garage_owner=user, is_active=True).exists()
