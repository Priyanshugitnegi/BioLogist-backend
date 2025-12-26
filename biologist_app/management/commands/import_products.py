import pandas as pd
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from biologist_app.models import Category, SubCategory, Product, ProductVariant


class Command(BaseCommand):
    help = "Import products from Excel (FINAL, safe & idempotent)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            required=True,
            help="Path to Excel file"
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        self.stdout.write(f"\n📄 Reading Excel: {file_path}\n")

        df = pd.read_excel(file_path)

        df.columns = (
            df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Columns detected: {list(df.columns)}")
        )

        def clean(value):
            if pd.isna(value):
                return ""
            return str(value).strip()

        def clean_price(value):
            if pd.isna(value):
                return None
            value = str(value).strip().lower()
            if value in ["por", "p.o.r", "n/a", "na", ""]:
                return None
            try:
                return Decimal(value)
            except (InvalidOperation, ValueError):
                return None

        created_products = 0
        created_variants = 0

        for _, row in df.iterrows():
            product_name = clean(row.get("product_name"))
            category_name = clean(row.get("category"))
            subcategory_name = clean(row.get("subcategory"))
            catalog_number = clean(row.get("catalog_no") or row.get("catalog_number"))
            unit = clean(row.get("quantity") or row.get("unit"))
            price = clean_price(row.get("price"))

            if not product_name or not catalog_number:
                continue

            category, _ = Category.objects.get_or_create(
                name=category_name or "Uncategorized"
            )

            subcategory = None
            if subcategory_name:
                subcategory, _ = SubCategory.objects.get_or_create(
                    name=subcategory_name,
                    category=category
                )

            product, created = Product.objects.get_or_create(
                name=product_name,
                category=category,
                subcategory=subcategory
            )

            if created:
                created_products += 1

            # 🔑 FIXED VARIANT LOGIC
            variant, v_created = ProductVariant.objects.update_or_create(
                catalog_number=catalog_number,
                defaults={
                    "product": product,
                    "unit": unit,
                    "price": price,
                }
            )

            if v_created:
                created_variants += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Import complete!\n"
                f"Products created: {created_products}\n"
                f"Variants created: {created_variants}\n"
            )
        )
