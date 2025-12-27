from django.urls import path
from .views import home

urlpatterns = [
    path("", home),
    path("products/", home),
    path("product/<slug:slug>/", home),
    path("contact/", home),

    # Catch-all for React Router
    path("<path:path>/", home),
]
