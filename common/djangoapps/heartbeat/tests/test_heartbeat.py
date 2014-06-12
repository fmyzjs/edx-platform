"""
Test the heartbeat
"""
import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
import json
from django.db.utils import DatabaseError
import mock

class HeartbeatTest(unittest.TestCase):
    """
    Test the heartbeat
    """

    def setUp(self):
        self.client = Client()
        self.heartbeat_url = reverse('heartbeat')
        return super(HeartbeatTest, self).setUp()

    def tearDown(self):
        return super(HeartbeatTest, self).tearDown()

    def test_success(self):
        response = self.client.get(self.heartbeat_url)
        self.assertEqual(response.status_code, 200)

    def test_sql_fail(self):
        with mock.patch('heartbeat.views.connection') as mock_connection:
            mock_connection.cursor.return_value.execute.side_effect = DatabaseError
            response = self.client.get(self.heartbeat_url)
            self.assertEqual(response.status_code, 503)
            response_dict = json.loads(response.content)
            self.assertIn('SQL', response_dict)

    def test_mongo_fail(self):
        with mock.patch('pymongo.MongoClient.alive', return_value=False):
            response = self.client.get(self.heartbeat_url)
            self.assertEqual(response.status_code, 503)
