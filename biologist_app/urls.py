from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ProductViewSet,
    TeamMemberViewSet,
    CategoryViewSet,
    EnquiryCreateView,
    ProductDetailBySlug,
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

    # ================= AUTH (JWT) =================
    path("api/auth/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),

    # 🔥 SLUG-BASED PRODUCT DETAIL API
    path("api/products/slug/<slug:slug>/", ProductDetailBySlug.as_view()),

    # ================= REACT =================
    path("", home),
    path("products/", home),
    path("product/<slug:slug>/", home),
    path("contact/", home),

    # Catch-all (keep last)
    path("<path:path>/", home),
]
