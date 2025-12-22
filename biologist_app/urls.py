from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet,
    TeamMemberViewSet,
    CategoryViewSet,
    EnquiryCreateView,
    home,
)

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("team", TeamMemberViewSet, basename="team")

urlpatterns = [
    # ================= API =================
    path("api/", include(router.urls)),
    path("api/enquiry/", EnquiryCreateView.as_view()),

    # ================= REACT =================
    path("", home),
    path("products/", home),
    path("product/<int:pk>/", home),
    path("contact/", home),

    # Catch-all
    path("<path:path>/", home),
]
