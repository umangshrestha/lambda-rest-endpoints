from unittest import TestCase
import requests

from tests.config import base_url




def TestApiGateway(TestCase):

    def test_hello(self):
        data = requests.get(f"{base_url}/hello").json()
        self.assertEqual(data['message'], "Hello, World!")

    def test_hello_name(self):
        data = requests.get(f"{base_url}/hello?name=Lambda").json()
        self.assertEqual(data['message'], "Hello, Lambda!")