from django.db import models
from ..constants import Status

class Sevice(models.Model):
    customer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_service_users_id')
    work_by = models.ForeignKey('Worker', on_delete=models.CASCADE, related_name='fk_worker_service_workers_id')
    status = models.IntegerField(
        choices=[(status.value, status.name) for status in Status],
        blank=True, null=True
    )

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"

