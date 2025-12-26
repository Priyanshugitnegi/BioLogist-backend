from rest_framework import serializers
from .models import (
    Product,
    ProductVariant,
    Category,
    SubCategory,
    TeamMember,
    Enquiry,
)


# =========================
# SUBCATEGORY SERIALIZER
# =========================
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
        ]


# =========================
# CATEGORY SERIALIZER
# =========================
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "product_count",
            "subcategories",
        ]


# =========================
# PRODUCT VARIANT SERIALIZER ✅ FIXED
# =========================
class ProductVariantSerializer(serializers.ModelSerializer):
    display_label = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "catalog_number",
            "quantity",
            "unit",
            "price",
            "is_default",
            "display_label",
        ]

    def get_display_label(self, obj):
        # quantity is now a STRING, not a number
        if obj.unit:
            return f"{obj.quantity} {obj.unit}"
        return obj.quantity


# =========================
# PRODUCT SERIALIZER
# =========================
class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )
    category_slug = serializers.CharField(
        source="category.slug",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "category",
            "category_name",
            "category_slug",
            "subcategory",
            "subcategory_name",
            "variants",
        ]


# =========================
# TEAM MEMBER SERIALIZER
# =========================
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "role",
            "image",
            "order",
            "is_active",
        ]


# =========================
# ENQUIRY SERIALIZER
# =========================
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"
