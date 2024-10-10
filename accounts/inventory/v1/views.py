import logging
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.authentication.v1.serializers import AccountsLoginSerializer, AccountsUserRegistrationSerializer
from accounts.inventory.v1.serializers import ItemSerializer
from accounts.models import ItemModel
from accounts.permissions import IsAdmin, IsReadOnly, IsWriteOnly
from core.settings import logger
from core.utils.generic_mixins import ResponseMixin
from django.http import Http404
from django.core.cache import cache

class CreateItemView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsWriteOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "CreateItemView"}
    )
    def post(self, request):
        try:
            serializer = ItemSerializer(data=request.data)
            if ItemModel.objects.filter(name=request.data.get('name')).exists():
                return Response({"error": "Item already exists."}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                self.api_logger.info("New Item added to inventory")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.api_logger.error(f"CreateItemView POST, {str(e)}")
            return self.error_response(data=str(e))


class ReadItemView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsWriteOnly | IsReadOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "ReadItemView"}
    )
    def get_object(self, item_id):
        # Check if the item is cached
        cached_item = cache.get(f'item_{item_id}')
        if cached_item:
            return cached_item

        try:
            item = ItemModel.objects.get(pk=item_id)
            cache.set(f'item_{item_id}', item, timeout=300)  # Cache timeout 5 mins
            return item
        except ItemModel.DoesNotExist:
            return None

    def get(self, request, item_id):
        try:
            item = self.get_object(item_id)
            if not item:
                return Response({"message" : "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Exception as e:
            self.api_logger.error(f"ReadItemView GET, {str(e)}")
            return self.error_response(data=str(e))

class UpdateItemView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsWriteOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "UpdateItemView"}
    )
    def get_object(self, item_id):
        try:
            return ItemModel.objects.get(pk=item_id)
        except ItemModel.DoesNotExist:
            return None

    def put(self, request, item_id):
        try:
            item = self.get_object(item_id)
            if not item:
                return Response({"message" : "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ItemSerializer(item, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                self.api_logger.info(f"Updated item {item_id} in inventory")

                cache.set(f'item_{item_id}', item, timeout=300)

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.api_logger.error(f"UpdateItemView PUT, {str(e)}")
            return self.error_response(data=str(e))


class DeleteItemView(views.APIView, ResponseMixin):
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsWriteOnly]
    api_logger = logging.LoggerAdapter(
        logger, {"app_name": "DeleteItemView"}
    )
    def get_object(self, item_id):
        try:
            return ItemModel.objects.get(pk=item_id)
        except ItemModel.DoesNotExist:
            return None

    def delete(self, request, item_id):
        try:
            item = self.get_object(item_id)
            if not item:
                return Response({"message" : "Item not found"}, status=status.HTTP_404_NOT_FOUND)
            item.delete()
            self.api_logger.info(f"Deleted item {item_id} in inventory")
            # Invalidate the cache after deleting the item
            cache.delete(f'item_{item_id}')

            return Response({"message": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            self.api_logger.error(f"DeleteItemView DELETE, {str(e)}")
            return self.error_response(data=str(e))