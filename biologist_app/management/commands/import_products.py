import pandas as pd

from django.core.management.base import BaseCommand
from django.db import transaction

from biologist_app.models import (
    Product,
    ProductVariant,
    Category,
    SubCategory,
)


def clean(value):
    """
    Converts NaN / empty / 'nan' → None
    Strips strings safely
    """
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() == "nan":
        return None

    return value


class Command(BaseCommand):
    help = "Import products & variants from Excel (NaN-safe, auto-category)"

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
            help="Excel file path"
        )

    def handle(self, *args, **options):
        file_path = options["file"]
        self.stdout.write(self.style.NOTICE(f"📂 Reading file: {file_path}"))

        df = pd.read_excel(file_path)

        created_products = 0
        created_variants = 0
        skipped_duplicates = 0
        failed_rows = 0

        # Ensure default category exists
        default_category, _ = Category.objects.get_or_create(
            name="Uncategorized",
            defaults={"slug": "uncategorized"}
        )

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # ============================
                    # REQUIRED FIELDS
                    # ============================
                    catalog_number = clean(row.get("catalog_number"))
                    product_name = clean(row.get("product_name"))

                    if not catalog_number or not product_name:
                        raise ValueError("Missing catalog number or product name")

                    # ============================
                    # CATEGORY (AUTO-FALLBACK)
                    # ============================
                    category_name = clean(row.get("category"))
                    category = default_category

                    if category_name:
                        category, _ = Category.objects.get_or_create(
                            name=category_name,
                            defaults={
                                "slug": category_name.lower().replace(" ", "-")
                            }
                        )

                    # ============================
                    # SUBCATEGORY (OPTIONAL)
                    # ============================
                    subcategory = None
                    subcategory_name = clean(row.get("subcategory"))

                    if subcategory_name:
                        subcategory, _ = SubCategory.objects.get_or_create(
                            category=category,
                            name=subcategory_name
                        )

                    # ============================
                    # PRODUCT (GROUPED BY NAME)
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
                    # DUPLICATE VARIANT CHECK
                    # ============================
                    if ProductVariant.objects.filter(
                        catalog_number=catalog_number
                    ).exists():
                        skipped_duplicates += 1
                        continue

                    # ============================
                    # QUANTITY (DEFAULT = 1)
                    # ============================
                    quantity = row.get("quantity")
                    quantity = int(quantity) if not pd.isna(quantity) else 1

                    # ============================
                    # UNIT (DEFAULT = "units")
                    # ============================
                    unit = clean(row.get("unit")) or "units"

                    # ============================
                    # PRICE (OPTIONAL)
                    # ============================
                    price = row.get("price")
                    price = float(price) if not pd.isna(price) else None

                    # ============================
                    # CREATE VARIANT
                    # ============================
                    ProductVariant.objects.create(
                        product=product,
                        catalog_number=catalog_number,
                        quantity=quantity,
                        unit=unit,
                        price=price,
                    )

                    created_variants += 1

                except Exception as e:
                    failed_rows += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️ Row {index + 1} skipped: {str(e)}"
                        )
                    )

        # ============================
        # SUMMARY
        # ============================
        self.stdout.write(self.style.SUCCESS("\n✅ IMPORT COMPLETE"))
        self.stdout.write(f"• Products created: {created_products}")
        self.stdout.write(f"• Variants created: {created_variants}")
        self.stdout.write(f"• Variants skipped (duplicates): {skipped_duplicates}")
        self.stdout.write(f"• Rows failed: {failed_rows}")
