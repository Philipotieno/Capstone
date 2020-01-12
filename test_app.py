import unittest
import os
import json
from app import create_app, db


class ActorsMoviesTestCase(unittest.TestCase):
    """ActorsMoviesTestCase test case"""

    def setUp(self):
        """Defines test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # Valid actor detaills
        self.actor = {
            "name": "test actor",
            "age": 12,
            "gender": "male"
        }

        # Invalid actor's age
        self.actor_one = {
            "name": "test actor",
            "age": 412,
            "gender": "male"
        }

        # Missing body part
        self.actor_two = {
            "name": "test actor",
            "gender": "male"
        }

        self.movie = {
            "name": "test actor",
            "age": 12,
            "gender": "male"
        }

        # Binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_create_actor(self):
        """Test Valid Post request for an actor"""
        res = self.client().post('/actors', json=self.actor)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_400_create_actor(self):
        """Test invalid age Post request for an actor"""
        res = self.client().post('/actors', json=self.actor_one)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            data['message'], 'Please input a valid age between 1-105!')

    def test_400_create_actor(self):
        """Test Post request for an actor with a missing field"""
        res = self.client().post('/actors', json=self.actor_two)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'Bad request')

    def test_409_create_actor(self):
        """Test Post request for an actor who has already been posted"""

        # post an actor
        self.client().post('/actors', json=self.actor)

        # post the same actor again
        res = self.client().post('/actors', json=self.actor)
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'Duplicate found')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
