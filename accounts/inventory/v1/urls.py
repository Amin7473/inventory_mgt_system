from django.contrib import admin
from django.urls import path
from accounts.inventory.v1 import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('create-item/', views.CreateItemView.as_view(), name='create-item'),
    path('get-item/<str:item_id>/', views.ReadItemView.as_view(), name='read-item'),
    path('update-item/<str:item_id>/', views.UpdateItemView.as_view(), name='update-item'),
    path('delete-item/<str:item_id>/', views.DeleteItemView.as_view(), name='delete-item'),
]