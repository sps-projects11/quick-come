import json
from django.shortcuts import get_object_or_404
from qcome.models import Payment, Booking,User,Worker
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from ..constants import PayType

    
def get_all_payments_created_by(user_id):
    """Retrieve all payments"""
    payments = Payment.objects.filter(created_by=user_id, is_active=True).values(
        'id', 'amount', 'type', 'paid_at', 'created_by__first_name', 'created_by__last_name','booking_id',
    )
    return list(payments)

def get_current_payment(booking_id):
    """Retrieve all payments"""
    payment = Payment.objects.filter(booking_id=booking_id,is_active=True).values()
    return list(payment)

def create_payment(request, booking_id, user_id):
    """Create a new payment for a given booking and deactivate the booking"""
    try:
        # Ensure it's a POST request
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

        data = json.loads(request.body)

        # Get the booking
        booking = Booking.objects.filter(id=booking_id, is_active=True).first()
        if not booking:
            return JsonResponse({"error": "❌ Booking not found or already inactive"}, status=400)

        # Get the user
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "❌ User not found"}, status=400)

        # Validate required fields
        required_fields = ['type', 'amount', 'pay_status']
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Create payment
        payment = Payment.objects.create(
            booking_id=booking,
            type=data.get('type'),
            amount=data.get('amount'),
            pay_status=data.get('pay_status'),
            created_by=user,
        )

        # Deactivate the booking
        booking.is_active = False
        booking.save(update_fields=["is_active"])

        response_data = {
            "message": "✅ Payment created successfully",
            "payment_id": payment.id
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
    
def payment_details_by_payment_id(payment_id):
    return Payment.objects.filter(id=payment_id, is_active=True).values(
        'id', 'amount', 'type', 'paid_at', 'created_by__first_name', 'created_by__last_name','booking_id',
    ).first()  # This ensures only one result is returned


def get_worker_payments(worker_user_id):
    """Retrieve payments for a worker if they are of type CASH."""
    worker_id=Worker.objects.filter(worker=worker_user_id).first()
    all_bookings_by_worker = Booking.objects.filter(assigned_worker=worker_id.id)
    payments = []
    for booking in all_bookings_by_worker:
        payment = Payment.objects.filter(
            booking_id=booking.id, 
            type=PayType.CASH.value,  # Ensures only CASH payments are considered
            is_active=True
        ).first()  # Fetch a single matching payment

        if payment:
            payments.append({
                "payment_id": payment.id,
                "amount": payment.amount,
                "paid_at": payment.paid_at.strftime('%Y-%m-%d'),
                "booking_id": booking.id,
                "customer": f"{booking.customer.first_name} {booking.customer.last_name}",
                "created_by": f"{payment.created_by.first_name} {payment.created_by.last_name}",
            })

    return payments



def get_all_payments():
    """Retrieve and customize all active payments."""
    # Use select_related to join Payment -> Booking -> assigned_worker -> worker (User)
    payments = Payment.objects.filter(is_active=True)\
        .select_related('booking_id__assigned_worker__worker')\
        .values(
            'id', 
            'amount', 
            'type', 
            'paid_at', 
            'created_by__first_name', 
            'created_by__last_name',
            'booking_id',
            'booking_id__assigned_worker__worker__first_name',
            'booking_id__assigned_worker__worker__last_name',
        )
    
    payments_data = []
    for payment in payments:
        # Convert the numeric payment type to its enum name
        payment_type = PayType(payment['type']).name if payment['type'] else "N/A"
        # Format the paid_at field as a string
        paid_at = payment['paid_at'].strftime('%Y-%m-%d %H:%M:%S') if payment['paid_at'] else "N/A"
        # Combine the created_by first and last name
        payment_by = f"{payment.get('created_by__first_name', '')} {payment.get('created_by__last_name', '')}".strip()
        
        # Determine 'paid_to' from the booking's assigned worker
        assigned_worker_first_name = payment.get('booking_id__assigned_worker__worker__first_name')
        assigned_worker_last_name = payment.get('booking_id__assigned_worker__worker__last_name')
        
        if assigned_worker_first_name:
            paid_to = f"{assigned_worker_first_name} {assigned_worker_last_name}".strip()
        else:
            paid_to = "Unknown"
        
        # Build custom payment dictionary.
        payment_data = {
            'payment_id': payment['id'],
            'amount': payment['amount'],
            'payment_type': payment_type,
            'paid_at': paid_at,
            'payment_by': payment_by,
            'booking_id': payment['booking_id'],
            'paid_to': paid_to,
        }
        payments_data.append(payment_data)
    
    return payments_data
