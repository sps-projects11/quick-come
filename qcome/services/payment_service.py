import json
from django.shortcuts import get_object_or_404
from qcome.models import Payment, Booking,User

    
def get_all_payments(user_id):
    """Retrieve all payments"""
    payments = Payment.objects.filter(created_by=user_id, is_active=True).values(
        'id', 'amount', 'type', 'paid_at', 'created_by__first_name', 'created_by__last_name'
    )
    return list(payments)

def get_current_payment(booking_id):
    """Retrieve all payments"""
    payment = Payment.objects.filter(booking_id=booking_id,is_active=True).values()
    return list(payment)

def create_payment(request, booking_id):
    """Create a new payment for a given booking"""
    try:
        data = json.loads(request.body)
        print("✅ Received Payment Data:", data)  # Debugging

        booking = Booking.objects.filter(id=booking_id).first()
        print("Booking:", booking)
        if not booking:
            return {"error": "❌ Booking not found"}

        # Ensure created_by is an integer
        created_by_id = int(data.get('created_by'))  # Convert to int
        print("Created_by ID:", created_by_id)

        # Fetch the actual User instance
        user = User.objects.get(id=created_by_id)  # Use get() to ensure a single User instance
        print("User:", user, "Type:", type(user))

        # Create payment
        payment = Payment.objects.create(
            booking_id=booking,
            type=data.get('type'),
            bank_ac=data.get('bank_ac') or None,
            amount=data.get('amount'),
            pay_status=data.get('pay_status'),
            created_by=user,  # Ensure we pass a User instance
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

