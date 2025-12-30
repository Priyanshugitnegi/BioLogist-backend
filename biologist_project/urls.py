from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 🔐 JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 🔐 AUTH (CUSTOMERS)
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 🔥 APP ROUTES
    path("", include("biologist_app.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
