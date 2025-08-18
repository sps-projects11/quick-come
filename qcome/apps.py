from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

class QcomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qcome'

    def ready(self):
        def create_admin(sender, **kwargs):
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='modaksubham69@gmail.com',
                    password='123456',
                    dob='2005-08-17',
                    roles=1
                )

        post_migrate.connect(create_admin)