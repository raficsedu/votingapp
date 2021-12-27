from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


# Create your tests here.
class AuthenticateUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        valid_employer = {
            'first_name': 'John',
            'last_name': 'Ibrahim',
            'email': 'employer1@myapp.com',
            'password': '@mypass45',
            'age': 33,
            'gender': 1,  # (Male=1, Female=2, Other=3)
            'phone': '01719454466'
        }
        client.post('/api/employer/list', valid_employer, format='json')

        valid_restaurant = {
            'name': 'Sharma House',
            'email': 'restaurant1@myapp.com',
            'password': '@mypass45',
            'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
            'phone': '01719454466'
        }
        client.post('/api/restaurant/list', valid_restaurant, format='json')

    def setUp(self):
        self.client = APIClient()

    def test_valid_employer_authentication(self):
        response = self.client.post('/api/authenticate',
                         {'email': 'employer1@myapp.com', 'password': '@mypass45'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_employer_authentication(self):
        response = self.client.post('/api/authenticate',
                         {'email': 'employer1@myapp.com', 'password': '@mypass45-1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_restaurant_authentication(self):
        response = self.client.post('/api/authenticate',
                                    {'email': 'restaurant1@myapp.com', 'password': '@mypass45'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_restaurant_authentication(self):
        response = self.client.post('/api/authenticate',
                                    {'email': 'restaurant1@myapp.com', 'password': '@mypass45-1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
