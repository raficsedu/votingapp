from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Entity
from .serializers import EmployerSerializer


# Create your tests here.
class CreateNewEmployerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_employer = {
            'first_name': 'John',
            'last_name': 'Ibrahim',
            'email': 'employer@myapp.com',
            'password': '@mypass45',
            'age': 33,
            'gender': 1,  # (Male=1, Female=2, Other=3)
            'phone': '01719454466'
        }
        self.duplicate_email = {
            'first_name': 'John',
            'last_name': 'Ibrahim',
            'email': 'employer@myapp.com',
            'password': '@mypass45',
            'age': 33,
            'gender': 1,  # (Male=1, Female=2, Other=3)
            'phone': '01719454466'
        }
        self.invalid_gender = {
            'first_name': 'John',
            'last_name': 'Ibrahim',
            'email': 'employer1@myapp.com',
            'password': '@mypass45',
            'age': 33,
            'gender': 5,  # (Male=1, Female=2, Other=3)
            'phone': '01719454466'
        }
        self.missing_required = {
            'first_name': 'John',
            'last_name': 'Ibrahim',
            'email': '',
            'password': '',
            'age': 33,
            'gender': 5,  # (Male=1, Female=2, Other=3)
            'phone': '01719454466'
        }

    def test_valid_employer_create(self):
        response = self.client.post('/api/employer/list', self.valid_employer, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_email(self):
        self.client.post('/api/employer/list', self.valid_employer, format='json')
        response = self.client.post('/api/employer/list', self.duplicate_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_gender(self):
        response = self.client.post('/api/employer/list', self.invalid_gender, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field(self):
        response = self.client.post('/api/employer/list', self.missing_required, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveEmployerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        for i in range(1, 6):
            valid_employer = {
                'first_name': 'John',
                'last_name': 'Ibrahim',
                'email': 'employer'+str(i)+'@myapp.com',
                'password': '@mypass45',
                'age': 33,
                'gender': 1,  # (Male=1, Female=2, Other=3)
                'phone': '01719454466'
            }
            client.post('/api/employer/list', valid_employer, format='json')

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_employer(self):
        response = self.client.get('/api/employer/list', format='json')
        employee = Entity.objects.all()
        serializer = EmployerSerializer(employee, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
