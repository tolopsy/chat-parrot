from rest_framework.test import APITestCase
from .views import get_access_token, get_random, get_refresh_token
from .models import User

class TestGenericFunctions(APITestCase):

    def test_get_random(self):
        random1 = get_random(12)
        random2 = get_random(14)
        random3 = get_random(12)

        # check that we are getting a result
        self.assertTrue(random1)

        # check that random1 is not equal to random3
        self.assertNotEqual(random1, random3)

        # check that the length of result returned is equal to what was specified
        self.assertEqual(len(random2), 14)
        self.assertEqual(len(random3), 12)

    
    def test_access_token(self):
        payload = {
            "id": 1
        }

        token = get_access_token(payload)

        self.assertTrue(token)


    def test_get_refresh_token(self):
        token = get_refresh_token()
        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url =  '/user/login'
    register_url = '/user/register'
    refresh_url = '/user/refresh'

    def test_register(self):
        payload = {
            "username": "testuser",
            "password": "testpass",
        }

        response  = self.client.post(self.register_url, data=payload)
        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        payload = {
            "username": "testuser",
            "password": "testpass",
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response  = self.client.post(self.login_url, data=payload)
        result  = response.json()

        # checks that status code is 200
        self.assertEqual(response.status_code, 200)

        # check that we obtain both access and refresh token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    
    def test_refresh(self):
        payload = {
            "username": "testuser",
            "password": "testpass",
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response  = self.client.post(self.login_url, data=payload)
        refresh  = response.json()["refresh"]

        # get refresh
        response  = self.client.post(self.refresh_url, data={"refresh": refresh})
        result = response.json()

        # checks that status code is 200
        self.assertEqual(response.status_code, 200)

        # check that we obtain both access and refresh token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserProfile(APITestCase):
    profile_url = "user/profile"

    def setUp(self):
        self.user = User.objects.create(username="toluboy", password="toluboy")
        self.client.force_authentication(user=self.user)