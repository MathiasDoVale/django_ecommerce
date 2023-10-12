from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product
from http import HTTPStatus

User = get_user_model()

# Create your tests here.
class ProductTestCase(TestCase):

    def setUp(self):

            # Create a staff user
            test_user1 = User.objects.create_user(email='testuser1@gmail.com', password='1X<ISRUkw+tuK', is_staff=True)
            test_user1.save()

    def test_product_add_n_times(self):
        """Add same product based on quantity number"""

        # Checking that staff user can visualize page
        login = self.client.login(username='testuser1@gmail.com', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        # Checking add same product based on quantity times
        response = self.client.post(reverse('add_product'), data={'name': 'test_name',
                                                             'description': 'test_description',
                                                             'price': 24,
                                                             'quantity': 3,
                                                             'size': 1})
        
        self.assertEqual(response.status_code, 200)
        products = Product.objects.all().count()
        self.assertEqual(products, 3)
            
        



        