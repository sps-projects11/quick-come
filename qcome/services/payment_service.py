import json
from django.shortcuts import get_object_or_404
from qcome.models import Payment, Booking

    
def get_all_payments(user_id):
    """Retrieve all payments"""
    payments = Payment.objects.filter(created_by=user_id).values()
    return list(payments)

def create_payment(request, booking_id):
    """Create a new payment for a given booking"""
    try:
        data = json.loads(request.body)
        print("✅ Received Payment Data:", data)  # Debugging

        booking = get_object_or_404(Booking, id=booking_id)

        payment = Payment.objects.create(
            booking=booking,
            type=data.get('type'),
            bank_ac=data.get('bank_ac'),
            amount=data.get('amount'),
            pay_status=data.get('pay_status'),
            created_by_id=data.get('created_by'),
        )

        return {"message": "✅ Payment created successfully", "payment_id": payment.id}
    except Exception as e:
        return {"error": str(e)}

def update_payment(request, booking_id):
    """Update an existing payment"""
    try:
        data = json.loads(request.body)
        payment = get_object_or_404(Payment, booking_id=booking_id)

        payment.type = data.get('type', payment.type)
        payment.bank_ac = data.get('bank_ac', payment.bank_ac)
        payment.amount = data.get('amount', payment.amount)
        payment.pay_status = data.get('pay_status', payment.pay_status)
        payment.save()

        return {"message": "Payment updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def delete_payment(booking_id):
    """Soft delete a payment (mark as inactive)"""
    try:
        payment = get_object_or_404(Payment, booking_id=booking_id)
        payment.is_active = False  # Correctly update the field
        payment.save()  # Save changes to the database

        return {"message": "Payment deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

