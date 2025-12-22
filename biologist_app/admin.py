from django.contrib import admin
from .models import (
    Product,
    ProductVariant,
    Category,
    SubCategory,
    TeamMember,
    Enquiry,        # ✅ ADD THIS
)


# ============================
# PRODUCT VARIANT INLINE
# ============================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = (
        "catalog_number",
        "quantity",
        "unit",
        "price",
        "is_default",
    )
    ordering = ("quantity",)


# ============================
# PRODUCT ADMIN
# ============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "subcategory",
        "is_new",
    )

    list_filter = (
        "category",
        "subcategory",
        "is_new",
    )

    search_fields = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    inlines = [ProductVariantInline]


# ============================
# CATEGORY ADMIN
# ============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


# ============================
# SUBCATEGORY ADMIN
# ============================
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)


# ============================
# ENQUIRY ADMIN  ✅ NEW
# ============================
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "product",
        "variant",
        "created_at",
    )

    list_filter = (
        "created_at",
        "product",
    )

    search_fields = (
        "name",
        "email",
        "variant__catalog_number",
        "product__name",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)


# ============================
# TEAM MEMBER ADMIN
# ============================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "role",
        "order",
        "is_active",
    )
    list_editable = (
        "order",
        "is_active",
    )
    ordering = ("order",)
