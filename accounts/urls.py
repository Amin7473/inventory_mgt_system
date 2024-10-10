from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/authentication/v1/", include("accounts.authentication.v1.urls")),
    path("api/inventory/v1/", include("accounts.inventory.v1.urls")),
]
