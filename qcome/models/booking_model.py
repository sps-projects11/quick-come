from django.db import models
from ..constants import Vehicle_Type
from django.db.models import Q, UniqueConstraint

class Booking(models.Model):
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_users_id')
    vehicle_type = models.IntegerField(
        choices=[(v_type.value, v_type.name) for v_type in Vehicle_Type],
        blank=False, null=False
    )
    current_location = models.CharField(max_length=255, null=False, blank=False)
    service = models.ForeignKey('ServiceCatalog', on_delete=models.CASCADE, blank=False, null=False)


    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_created_users_id')
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_updated_users_id')


    class Meta:
        db_table = 'bookings'
        constraints =[
            UniqueConstraint(
            fields=['customer'],
            condition=Q(is_active=True),
            name='unique_active_booking_per_user'
            )
        ]


    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"