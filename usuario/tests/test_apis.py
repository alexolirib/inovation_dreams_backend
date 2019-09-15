import os
import json
from django.test import TestCase, Client
from django.urls import reverse


class CreateUserTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fixtures = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'fixtures')

    def test_create_user(self):
        data = open(os.path.join(self.fixtures, 'criar_usuario.json')).read()
        response = self.client.post(reverse('create_user'), data)
        self.assertEquals(response.status_code, 201)
