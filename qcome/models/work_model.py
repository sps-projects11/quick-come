from django.db import models
from ..constants import Status

class Work(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='fk_bookig_work_bookings_id')
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_work_users_id')
    work_by = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='fk_worker_work_workers_id')
    final_work_image = models.URLField(max_length=200, null=True, blank=True)
    status = models.IntegerField(
        choices=[(status.value, status.name) for status in Status],
        blank=True, null=True
    )
    work_photo_url = models.URLField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'works'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"

