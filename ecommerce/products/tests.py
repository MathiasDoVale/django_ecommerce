from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product, Inventory, Gender
from http import HTTPStatus

User = get_user_model()

# Create your tests here.
class ProductTestCase(TestCase):

    def setUp(self):

            # Create a staff user
            test_user1 = User.objects.create_user(email='testuser1@gmail.com', password='1X<ISRUkw+tuK', is_staff=True)
            test_user1.save()
            login = self.client.login(username='testuser1@gmail.com', password='1X<ISRUkw+tuK')

    def test_product_add_n_times_with_n_sizes(self):
        """Add product based on quantity number and 1 size"""

        # Checking that staff user can visualize page
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        # Checking product creation
        response = self.client.post(reverse('add_product'), data={'name': 'test_name',
                                                             'description': 'test_description',
                                                             'price': 24.5,
                                                             'quantity': 3,
                                                             'sizes': (5,6),
                                                             'genders': ('MEN', 'WOMEN')})
        
        self.assertEqual(response.status_code, 200)
        product = Product.objects.all()
        self.assertEqual(product.count(), 1)
        product = product.first()
        self.assertEqual(product.name, 'test_name') 
        self.assertEqual(product.description, 'test_description')
        self.assertEqual(product.price, 24.5)

        # Checking inventory (instances of the product)
        inventory_qty = Inventory.objects.all().count()
        self.assertEqual(inventory_qty, 6) # number of sizes * quantity
        inventory = Inventory.objects.filter(product_id=product.id)

        size_5 = inventory.filter(size='5')
        self.assertEqual(size_5.count(), 3)

        size_6 = inventory.filter(size='6')
        self.assertEqual(size_6.count(), 3)

        # Checking genders instances of the product
        gender_qty = Gender.objects.all().count()
        self.assertEqual(gender_qty, 2) # number of genders
        genders = Gender.objects.filter(product_id=product.id)

        men_gender = genders.filter(gender='MEN')
        self.assertEqual(men_gender.count(), 1)

        women_gender = genders.filter(gender='WOMEN')
        self.assertEqual(women_gender.count(), 1) 

