from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from biologist_app.views import (
    ProductViewSet,
    CategoryViewSet,
    TeamMemberViewSet,
    EnquiryCreateView,
    ProductDetailBySlug,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("team", TeamMemberViewSet, basename="team")

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ API (backend)
    path("api/v1/", include(router.urls)),
    path("api/v1/enquiry/", EnquiryCreateView.as_view()),
    path("api/v1/products/slug/<slug:slug>/", ProductDetailBySlug.as_view()),

    # ✅ FRONTEND (React / SPA)
    path("", include("biologist_app.urls")),
]
