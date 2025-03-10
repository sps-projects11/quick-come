from django.db import models

class Billing(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='fk_booking_billing_bookings_id')
    billing_by = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='fk_worker_billing_workers_id')
    service = models.ForeignKey('ServiceCatalog', on_delete=models.CASCADE, related_name='fk_service_billing_services_id')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)


    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True, null=True, blank=True)
    created_by = models.ForeignKey('Worker', on_delete=models.CASCADE, null=False, blank=True, related_name='fk_worker_billing_create_workers_id')
    updated_by = models.ForeignKey('Worker', on_delete=models.CASCADE, null=True, blank=True, related_name='fk_worker_billing_update_workers_id')


    class Meta:
        db_table = 'billings'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"