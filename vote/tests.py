from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from .models import Entity
from employer.models import Entity as E_Entity


# Create your tests here.
class CreateNewVoteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()

        # Create Employer
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

        # Create Restaurant
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
        self.valid_vote = {
            'restaurant': 1,
            'vote': 1
        }
        self.invalid_vote = {
            'restaurant': 11,
            'vote': 11
        }

        # Authenticate employer
        self.auth = self.client.post('/api/authenticate',
                                     {'email': 'employer1@myapp.com', 'password': '@mypass45'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth.data['token'])

    def test_valid_vote_create(self):
        response = self.client.post('/api/vote/list', self.valid_vote, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_vote_create(self):
        self.client.post('/api/vote/list', self.valid_vote, format='json')
        response = self.client.post('/api/vote/list', self.valid_vote, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_vote_create(self):
        response = self.client.post('/api/vote/list', self.invalid_vote, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VoteResultTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        day_before_yesterday = today - datetime.timedelta(days=2)

        # Create Employer
        for i in range(2, 8):
            valid_employer = {
                'first_name': 'John',
                'last_name': 'Ibrahim',
                'email': 'employer' + str(i) + '@myapp.com',
                'password': '@mypass45',
                'age': 33,
                'gender': 1,  # (Male=1, Female=2, Other=3)
                'phone': '01719454466'
            }
            client.post('/api/employer/list', valid_employer, format='json')

        # Create Restaurant
        for i in range(2, 5):
            valid_restaurant = {
                'name': 'Sharma House',
                'email': 'restaurant' + str(i) + '@myapp.com',
                'password': '@mypass45',
                'address': 'House 9/1-A, Kallyanpur, 1207, Dhaka',
                'phone': '01719454466'
            }
            client.post('/api/restaurant/list', valid_restaurant, format='json')

            # 'employer_id': 'restaurant_id'
            vote_mapping = {
                '2': 4,
                '3': 2,
                '4': 3,
                '5': 4,
                '6': 4,
                '7': 3,
            }

            # Make vote for 3 consecutive days
            for vote in vote_mapping:
                Entity.objects.create(employer_id=int(vote), restaurant_id=vote_mapping[vote], vote=1,
                                      created_at=day_before_yesterday)
                Entity.objects.create(employer_id=int(vote), restaurant_id=vote_mapping[vote], vote=1,
                                      created_at=yesterday)
                Entity.objects.create(employer_id=int(vote), restaurant_id=vote_mapping[vote], vote=1)

    def setUp(self):
        self.client = APIClient()
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.day_before_yesterday = self.today - datetime.timedelta(days=2)

        print(E_Entity.objects.all().values('id'))

        # Authenticate employer
        self.auth = self.client.post('/api/authenticate',
                                     {'email': 'employer2@myapp.com', 'password': '@mypass45'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth.data['token'])

    def test_today_vote_result(self):
        response = self.client.post('/api/vote/result', {'date': self.today}, format='json')
        self.assertEqual(response.data['restaurant_id'], 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_yesterday_vote_result(self):
        response = self.client.post('/api/vote/result', {'date': self.yesterday}, format='json')
        self.assertEqual(response.data['restaurant_id'], 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_day_before_yesterday_vote_result(self):
        response = self.client.post('/api/vote/result', {'date': self.day_before_yesterday}, format='json')
        self.assertEqual(response.data['restaurant_id'], 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
