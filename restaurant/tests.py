from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Entity
from .serializers import RestaurantSerializer


# Create your tests here.
class CreateNewRestaurantTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_restaurant = {
            'name': 'Sharma House',
            'email': 'restaurant@myapp.com',
            'password': '@mypass45',
            'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
            'phone': '01719454466'
        }
        self.duplicate_email = {
            'name': 'Sharma House',
            'email': 'restaurant@myapp.com',
            'password': '@mypass45',
            'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
            'phone': '01719454466'
        }
        self.missing_required = {
            'name': 'Sharma House',
            'email': '',
            'password': '',
            'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
            'phone': '01719454466'
        }

    def test_valid_restaurant_create(self):
        # Valid restaurant
        response = self.client.post('/api/restaurant/list', self.valid_restaurant, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_email(self):
        # With duplicate email
        self.client.post('/api/restaurant/list', self.duplicate_email, format='json')
        response = self.client.post('/api/restaurant/list', self.duplicate_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field(self):
        # Missing some required field
        response = self.client.post('/api/restaurant/list', self.missing_required, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveRestaurantTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        for i in range(1, 4):
            valid_restaurant = {
                'name': 'Sharma House',
                'email': 'restaurant'+str(i)+'@myapp.com',
                'password': '@mypass45',
                'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
                'phone': '01719454466'
            }
            client.post('/api/restaurant/list', valid_restaurant, format='json')

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_restaurant(self):
        response = self.client.get('/api/restaurant/list', format='json')
        restaurants = Entity.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewMenuTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a restaurant
        valid_restaurant = {
            'name': 'Sharma House',
            'email': 'restaurant@myapp.com',
            'password': '@mypass45',
            'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
            'phone': '01719454466'
        }
        self.restaurant = self.client.post('/api/restaurant/list', valid_restaurant, format='json')

        # Authenticate restaurant
        self.auth = self.client.post('/api/authenticate',
                                     {'email': self.restaurant.data['email'], 'password': '@mypass45'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth.data['token'])

        self.valid_menu = {
            'date': '',
            'menus': [
                {
                    'item': 'Polao',
                    'price': 100
                },
                {
                    'item': 'Roast',
                    'price': 150
                }
            ]
        }

    def test_valid_menu_create(self):
        # With 'date' field but empty
        response = self.client.post('/api/restaurant/menu/list', self.valid_menu, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Without 'date' field
        self.valid_menu.pop('date')
        response = self.client.post('/api/restaurant/menu/list', self.valid_menu, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_menu_create_for_a_target_date(self):
        # With specific date
        self.valid_menu['date'] = '2021-12-26'
        response = self.client.post('/api/restaurant/menu/list', self.valid_menu, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RetrieveMenuTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_menu = {
            'date': '',
            'menus': [
                {
                    'item': 'Polao',
                    'price': 100
                },
                {
                    'item': 'Roast',
                    'price': 150
                }
            ]
        }

        # Add data for 3 restaurant
        for i in range(1, 4):
            self.valid_restaurant = {
                'name': 'Sharma House',
                'email': 'restaurant' + str(i) + '@myapp.com',
                'password': '@mypass45',
                'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
                'phone': '01719454466'
            }
            self.restaurant = self.client.post('/api/restaurant/list', self.valid_restaurant, format='json')

            # Authenticate and add menu
            self.auth = self.client.post('/api/authenticate',
                                         {'email': self.restaurant.data['email'], 'password': '@mypass45'},
                                         format='json')
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth.data['token'])
            self.client.post('/api/restaurant/menu/list', self.valid_menu, format='json')

    def test_retrieve_menu(self):
        response = self.client.get('/api/restaurant/menu/list', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

