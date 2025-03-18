from django.db import models
from ..constants import Vehicle_Type
from django.db.models import Q, UniqueConstraint
from django.contrib.postgres.fields import ArrayField

class Booking(models.Model):
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_users_id')
    vehicle_type = models.IntegerField(
        choices=[(v_type.value, v_type.name) for v_type in Vehicle_Type],
    )
    current_location = models.CharField(max_length=255)
    service = ArrayField(
        models.IntegerField(),
        blank=False,
        null=False,
        default=list
    )
    description = models.CharField(blank=True,null=True,max_length=255)
    assigned_worker = models.ForeignKey('Worker', on_delete=models.CASCADE, null=True, blank=True, related_name='fk_worker_booking_workers_id')

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_created_users_id', blank=True, null=False)
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_bookings_updated_users_id', null=True, blank=True)


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