from ..models import Payment

def get_payment_list():
    bookings=Payment.objects.all()
    return bookings

def create_payment(payment_id):
    Payment.objects.create()
    return 

def update_payment(payment_id):
    Payment.objects.update()
    return

def delete_payment(payment_id):
    Payment.objects.update()
    return