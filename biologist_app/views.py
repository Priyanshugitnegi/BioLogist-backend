from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Min, Count
from django.shortcuts import get_object_or_404, render

from .models import (
    Product,
    TeamMember,
    Category,
    Enquiry,
)

from .serializers import (
    ProductSerializer,
    TeamMemberSerializer,
    CategorySerializer,
    EnquirySerializer,
)


# =========================
# REACT ENTRY
# =========================
def home(request, *args, **kwargs):
    return render(request, "home.html")


# =========================
# PRODUCTS (LIST + DETAIL)
# =========================
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    # 🔍 SEARCH + FILTER
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["category", "subcategory"]

    def get_queryset(self):
        base_qs = (
            Product.objects
            .select_related("category", "subcategory")
            .prefetch_related("variants")
            .order_by("name")
        )

        # LIST → group by product name
        if self.action == "list":
            grouped_ids = (
                base_qs
                .values("name")
                .annotate(first_id=Min("id"))
                .values_list("first_id", flat=True)
            )
            return base_qs.filter(id__in=grouped_ids)

        # DETAIL
        return base_qs

    def retrieve(self, request, pk=None):
        product = get_object_or_404(
            Product.objects
            .select_related("category", "subcategory")
            .prefetch_related("variants"),
            pk=pk
        )
        serializer = self.get_serializer(product)
        return Response(serializer.data)


# =========================
# PRODUCT DETAIL (BY SLUG)
# =========================
class ProductDetailBySlug(APIView):
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
            .annotate(product_count=Count("products", distinct=True))
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
