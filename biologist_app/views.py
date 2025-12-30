from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count, Exists, OuterRef, Case, When, IntegerField
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User

from .models import (
    Product,
    ProductVariant,
    TeamMember,
    Category,
    Enquiry,
)

from .serializers import (
    ProductSerializer,
    TeamMemberSerializer,
    CategorySerializer,
    EnquirySerializer,
    RegisterSerializer,   # ✅ ADD THIS
)

# =========================
# REACT ENTRY
# =========================
def home(request, *args, **kwargs):
    return render(request, "home.html")


# =========================
# AUTH – REGISTER (CUSTOMER)
# =========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]   # 🔥 FIXES 403


# =========================
# PRODUCTS (LIST + DETAIL)
# =========================
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["category", "subcategory"]

    def get_queryset(self):
        base_qs = (
            Product.objects
            .select_related("category", "subcategory")
            .prefetch_related("variants")
        )

        if self.action == "list":
            qs = base_qs.annotate(
                has_variants=Exists(
                    ProductVariant.objects.filter(product=OuterRef("pk"))
                )
            ).annotate(
                priority=Case(
                    When(has_variants=True, then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            ).order_by("name", "priority", "id")

            picked_ids = []
            seen = set()

            for product in qs:
                if product.name not in seen:
                    seen.add(product.name)
                    picked_ids.append(product.id)

            return base_qs.filter(id__in=picked_ids).order_by("name")

        return base_qs.order_by("name")


# =========================
# PRODUCT DETAIL (BY SLUG)
# =========================
class ProductDetailBySlug(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, slug):
        product = get_object_or_404(
            Product.objects
            .select_related("category", "subcategory")
            .prefetch_related("variants"),
            slug=slug
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)


# =========================
# CATEGORIES
# =========================
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return (
            Category.objects
            .annotate(
                product_count=Count("products__name", distinct=True)
            )
            .order_by("name")
        )


# =========================
# TEAM
# =========================
class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.order_by("order")
    serializer_class = TeamMemberSerializer


# =========================
# ENQUIRY API
# =========================
class EnquiryCreateView(APIView):
    def post(self, request):
        serializer = EnquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Enquiry submitted successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
