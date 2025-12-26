raise RuntimeError("IMPORT_PRODUCTS COMMAND WAS EXECUTED")

import pandas as pd
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from biologist_app.models import (
    Category,
    SubCategory,
    Product,
    ProductVariant,
)


class Command(BaseCommand):
    help = "Import categories, subcategories, products & variants from Excel file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to Excel file"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"\n📄 Reading Excel: {file_path}\n"))

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading file: {e}"))
            return

        created_products = 0
        created_variants = 0

        for _, row in df.iterrows():

            # ============================
            # CLEAN VALUES (EXACT EXCEL)
            # ============================
            product_name = str(row.get("Product name", "")).strip()
            category_name = str(row.get("category", "")).strip()
            subcategory_name = str(row.get("subcategory", "")).strip()

            variant_catalog = str(row.get("Catalog no", "")).strip()
            quantity = str(row.get("quantity", "")).strip()

            raw_price = str(row.get("price", "")).strip()
            price = float(raw_price) if raw_price.replace(".", "", 1).isdigit() else None

            if not product_name or not category_name:
                continue

            # ============================
            # CATEGORY (SAFE SLUG LOGIC)
            # ============================
            category = Category.objects.filter(name=category_name).first()

            if not category:
                base_slug = slugify(category_name)
                slug = base_slug
                counter = 1

                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                category = Category.objects.create(
                    name=category_name,
                    slug=slug
                )

            # ============================
            # SUBCATEGORY
            # ============================
            subcategory = None
            if subcategory_name:
                subcategory, _ = SubCategory.objects.get_or_create(
                    category=category,
                    name=subcategory_name
                )

            # ============================
            # PRODUCT
            # ============================
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    "category": category,
                    "subcategory": subcategory,
                }
            )

            if created:
                created_products += 1

            # ============================
            # VARIANT
            # ============================
            if variant_catalog:
                variant, variant_created = ProductVariant.objects.update_or_create(
                    catalog_number=variant_catalog,
                    defaults={
                        "product": product,
                        "quantity": quantity,
                        "unit": "",
                        "price": price,
                    }
                )

                if variant_created:
                    created_variants += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Import complete!"
            f"\n   🆕 Products created: {created_products}"
            f"\n   ➕ Variants created: {created_variants}\n"
        ))
