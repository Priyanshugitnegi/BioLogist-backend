import pandas as pd
from django.core.management.base import BaseCommand
from biologist_app.models import Product, ProductVariant

class Command(BaseCommand):
    help = "Import products and variants from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="Path to Excel file")

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path:
            self.stdout.write(self.style.ERROR("❌ Please provide --file argument"))
            return

        self.stdout.write(f"📄 Reading Excel: {file_path}")

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading file: {e}"))
            return

        for index, row in df.iterrows():
            product_name = str(row.get("product_name", "")).strip()
            category = str(row.get("category", "")).strip()
            description = str(row.get("description", "")).strip()

            variant_name = str(row.get("variant_name", "")).strip()
            price = row.get("price", 0)
            stock = row.get("stock", 0)

            if not product_name:
                self.stdout.write(self.style.WARNING(f"⚠️ Row {index} skipped (missing product_name)"))
                continue

            # CREATE PRODUCT
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    "category": category,
                    "description": description
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"🆕 Added product: {product_name}"))
            else:
                self.stdout.write(f"➡️ Product exists: {product_name}")

            # CREATE VARIANT
            if variant_name:
                ProductVariant.objects.create(
                    product=product,
                    name=variant_name,
                    price=price if price else 0,
                    stock=stock if stock else 0,
                )

                self.stdout.write(f"   ➕ Added variant: {variant_name}")

        self.stdout.write(self.style.SUCCESS("✅ Import completed!"))
