from django.db import models

class ServiceCatalog(models.Model):
    service_name = models.CharField(max_length=200)
    service_image = models.URLField(max_length=200, null=True, blank=True)
    spare_part = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        related_name='fk_user_service_created_users_id'
    )
    updated_by = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        related_name='fk_user_service_updated_users_id', 
        null=True, blank=True
    )


    class Meta:
        db_table = 'services'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"
