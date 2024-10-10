from rest_framework import serializers
from django.contrib.auth import get_user_model

from accounts.models import ItemModel
from core.utils.generic_utils import is_valid_password

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModel
        fields = ['id', 'name', 'description']

