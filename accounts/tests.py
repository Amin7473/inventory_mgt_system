from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import ItemModel
from django.core.cache import cache


class InventoryManagementTestCase(APITestCase):

    def setUp(self):
        """
        This method sets up the data required for testing.
        """
        self.user = get_user_model().objects.create_user(email = "testuser@mail,com", role = "ADMIN", username='testuser', password='testpass')
        # self.client.login(email = "testuser@mail,com", password='testpass')
        self.client.force_authenticate(user=self.user)
        self.item_data = {
            'name': 'Test Item',
            'description': 'Test description'
        }

        self.item = ItemModel.objects.create(name='Existing Item', description='Existing description')

        self.create_item_url = reverse('create-item') 
        self.read_item_url = reverse('read-item', kwargs={'item_id': self.item.id})
        self.update_item_url = reverse('update-item', kwargs={'item_id': self.item.id})
        self.delete_item_url = reverse('delete-item', kwargs={'item_id': self.item.id})

    def tearDown(self):
        """
        This method cleans up after each test.
        """
        cache.clear()  # clear Redis cache after every test

    def test_create_item(self):
        """
        Test creating a new item in the inventory.
        """
        response = self.client.post(self.create_item_url, self.item_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.item_data['name'])
        self.assertEqual(response.data['description'], self.item_data['description'])

    def test_create_item_already_exists(self):
        """
        Test attempting to create an item that already exists.
        """
        ItemModel.objects.create(name='Test Item', description='Another description')  # Create duplicate item

        response = self.client.post(self.create_item_url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Item already exists', response.data['error'])

    def test_read_item(self):
        """
        Test retrieving an item from the inventory.
        """
        response = self.client.get(self.read_item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)
        self.assertEqual(response.data['description'], self.item.description)

        cached_item = cache.get(f'item_{self.item.id}')
        self.assertIsNotNone(cached_item)
        self.assertEqual(cached_item.name, self.item.name)

    def test_read_item_not_found(self):
        """
        Test trying to read a non-existent item.
        """
        non_existent_item_url = reverse('read-item', kwargs={'item_id': "0e288ab1-4b85-464c-80a1-fd553041978b"})
        response = self.client.get(non_existent_item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_item_not_found(self):
        """
        Test trying to update a non-existent item.
        """
        non_existent_item_url = reverse('update-item', kwargs={'item_id': "0e288ab1-4b85-464c-80a1-fd553041978b"})
        response = self.client.put(non_existent_item_url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item(self):
        """
        Test deleting an existing item in the inventory.
        """
        response = self.client.delete(self.delete_item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ItemModel.DoesNotExist):
            ItemModel.objects.get(id=self.item.id)

        cached_item = cache.get(f'item_{self.item.id}')
        self.assertIsNone(cached_item)  # cache should be invalidated after the delete

    def test_delete_item_not_found(self):
        """
        Test trying to delete a non-existent item.
        """
        non_existent_item_url = reverse('delete-item', kwargs={'item_id': "0e288ab1-4b85-464c-80a1-fd553041978b"})
        response = self.client.delete(non_existent_item_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

