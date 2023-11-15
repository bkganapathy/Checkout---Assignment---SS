import unittest
from flask import Flask
from checkout_d import app

class CheckoutServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_insert_user(self):
        # Define the data to be sent in the request
        data = {
            'c_name': 'TestUser_one',
            'c_mobile': '9876543210',
            'c_address': 'TestAddress'
        }

        # Send a GET request to the insert_user endpoint
        response = self.app.get('/insert_user', query_string=data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected message
        expected_message = {'message': 'Order inserted successfully'}
        self.assertDictEqual(response.get_json(), expected_message)

    def test_process_order(self):
        # Send a GET request to the process_order endpoint
        response = self.app.get('/')

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
