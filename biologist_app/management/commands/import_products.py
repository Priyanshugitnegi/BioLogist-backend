from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Disabled in production"

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING("import_products is disabled in production")
        )
