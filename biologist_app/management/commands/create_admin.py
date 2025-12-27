from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create admin user on Render (one-time)"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "ram"
        password = "ram@123"
        email = "biologistservices@gmail.com"

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists"))
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            email=email
        )

        self.stdout.write(self.style.SUCCESS("✅ Admin user created successfully"))
