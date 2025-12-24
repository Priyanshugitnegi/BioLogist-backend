import pandas as pd
from django.core.management.base import BaseCommand
from biologist_app.models import (
    Category, SubCategory, Product, ProductVariant
)


class Command(BaseCommand):
    help = "Import categories, subcategories, products & variants from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="Path to Excel file")

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path:
            self.stdout.write(self.style.ERROR("❌ Please provide --file argument"))
            return

        self.stdout.write(f"\n📄 Reading Excel: {file_path}\n")

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error reading file: {e}"))
            return

        for index, row in df.iterrows():

            # --- CLEAN VALUES ---
            product_name = str(row.get("product_name", "")).strip()
            category_name = str(row.get("category", "")).strip()
            subcategory_name = str(row.get("subcategory", "")).strip()
            description = str(row.get("description", "")).strip()

            variant_catalog = str(row.get("catalog_number", "")).strip()
            quantity = row.get("quantity", None)
            unit = str(row.get("unit", "")).strip()
            price = row.get("price", None)

            if not product_name:
                self.stdout.write(self.style.WARNING(f"⚠️ Row {index} skipped (no product_name)"))
                continue

            # --- FIX "nan" values ---
            if category_name.lower() == "nan": category_name = ""
            if subcategory_name.lower() == "nan": subcategory_name = ""
            if description.lower() == "nan": description = ""

            # --- CATEGORY ---
            category_obj = None
            if category_name:
                category_obj, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={"slug": category_name.lower().replace(" ", "-")}
                )

            # --- SUBCATEGORY ---
            subcategory_obj = None
            if subcategory_name and category_obj:
                subcategory_obj, _ = SubCategory.objects.get_or_create(
                    category=category_obj,
                    name=subcategory_name
                )

            # --- PRODUCT ---
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    "category": category_obj,
                    "subcategory": subcategory_obj,
                    "description": description,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"🆕 Added product: {product_name}"))
            else:
                # Update category or subcategory if needed
                if product.category != category_obj:
                    product.category = category_obj
                if subcategory_obj and product.subcategory != subcategory_obj:
                    product.subcategory = subcategory_obj
                if description:
                    product.description = description
                product.save()
                self.stdout.write(f"➡️ Updated product: {product_name}")

            # --- VARIANT ---
            if variant_catalog:
                ProductVariant.objects.update_or_create(
                    catalog_number=variant_catalog,
                    defaults={
                        "product": product,
                        "quantity": quantity if quantity else 0,
                        "unit": unit,
                        "price": price if price else 0,
                    }
                )
                self.stdout.write(f"   ➕ Variant: {variant_catalog}")

        self.stdout.write(self.style.SUCCESS("\n✅ Import completed successfully!\n"))
