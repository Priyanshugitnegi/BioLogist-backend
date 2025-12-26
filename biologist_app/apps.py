from django.apps import AppConfig
import os

class BiologistAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "biologist_app"

    def ready(self):
        # 🚨 Prevent running twice
        if os.environ.get("RUN_MAIN") != "true":
            return

        from biologist_app.models import Product
        if Product.objects.exists():
            return  # ✅ DB already seeded

        try:
            from django.core.management import call_command
            print("🌱 Seeding database from Excel...")
            call_command(
                "import_products",
                file="data/product_7.xlsx"
            )
            print("✅ Database seeded successfully")
        except Exception as e:
            print("❌ Seeding failed:", e)
