import json
import os
import unittest

from app import create_app, db


class ActorsMoviesTestCase(unittest.TestCase):
    """ActorsMoviesTestCase test case"""

    def setUp(self):
        """Defines test variables and initialize app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # Valid actor details
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

        # Valid actor details
        self.actor_three = {
            "name": "test actor two",
            "age": 12,
            "gender": "male"
        }

        # Missing body part
        self.actor_two = {
            "name": "test actor",
            "gender": "male"
        }

        self.movie = {
            "title": "test movie",
            "release_date": "12-12-2022"
        }
        self.assistant = os.getenv('ASSISTANT')
        self.producer = os.getenv('PRODUCER')
        self.director = os.getenv('DIRECTOR')

        # Binds the app to the current context
        with self.app.app_context():
            db.create_all()

    def test_create_actor(self):
        """Test Valid Post request for an actor"""
        res = self.client().post('/actors',
                                 json=self.actor,
                                 headers={'Authorization': self.director})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_create_actor_no_auth(self):
        """Test Post request for an actor with no header auth"""
        res = self.client().post('/actors',
                                 json=self.actor)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.get_json()['success'], False)

    def test_400_create_actor(self):
        """Test invalid age Post request for an actor"""
        res = self.client().post('/actors',
                                 json=self.actor_one,
                                 headers={'Authorization': self.director})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['message'],
                         'Please input a valid age between 1-105!'
                         )

    def test_400_create_actor(self):
        """Test Post request for an actor with a missing field"""
        res = self.client().post('/actors',
                                 json=self.actor_two,
                                 headers={'Authorization': self.director})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'Bad request')

    def test_409_create_actor(self):
        """Test Post request for an actor who has already been posted"""

        # post an actor
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        # post the same actor again
        res = self.client().post('/actors',
                                 json=self.actor,
                                 headers={'Authorization': self.director})

        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.get_json()['success'], False)
        self.assertEqual(res.get_json()['message'], 'Duplicate found')

    def test_get_all_actors(self):
        """Test getting all actors"""
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        res = self.client().get('/actors',
                                headers={'Authorization': self.director})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_all_actors(self):
        """Test getting list of empty actors"""
        res = self.client().get('/actors',
                                headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_one_actor(self):
        """Test getting one actors"""
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        res = self.client().get('/actors/1',
                                headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_one_actor(self):
        """Test getting non existing actor"""
        res = self.client().get('/actors/1',
                                headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_one_actor(self):
        """Test deleting non existing actor"""
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        res = self.client().delete('/actors/1',
                                   headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_one_actor(self):
        """Test deleting one actors"""
        res = self.client().delete('/actors/1',
                                   headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_update_actors_details(self):
        """Test updating actors details"""
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        res = self.client().patch('/actors/1',
                                  json=self.actor_three,
                                  headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_409_update_actors_details_with_same_details(self):
        """Test updating actors details with same details"""
        self.client().post('/actors',
                           json=self.actor,
                           headers={'Authorization': self.director})

        res = self.client().patch('/actors/1',
                                  json=self.actor,
                                  headers={'Authorization': self.director})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['message'], 'details upto date')

    def test_post_movie(self):
        """Test Valid Post request for a movie"""
        res = self.client().post('/movies',
                                 json=self.movie,
                                 headers={'Authorization': self.producer})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_403_post_movie_non_role(self):
        """Test Posting a movie for a non authorised user RBAC"""
        res = self.client().post('/movies',
                                 json=self.movie,
                                 headers={'Authorization': self.director})

        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['success'], False)

    def test_get_all_movies(self):
        """Test getting all movies"""
        self.client().post('/movies',
                           json=self.movie,
                           headers={'Authorization': self.producer})

        res = self.client().get('/movies',
                                headers={'Authorization': self.producer})

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_all_movies(self):
        """Test getting list of empty movies"""
        res = self.client().get('/movies',
                                headers={'Authorization': self.producer})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_delete_one_movie(self):
        """Test deleteing a movie"""
        self.client().post('/movies',
                           json=self.movie,
                           headers={'Authorization': self.producer})

        res = self.client().delete('/movies/1',
                                   headers={'Authorization': self.producer})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_none_movies(self):
        """Test deleting non existing movie"""
        res = self.client().delete('/movies/1',
                                   headers={'Authorization': self.producer})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_one_movie(self):
        """Test getting one movie"""
        self.client().post('/movies',
                           json=self.movie,
                           headers={'Authorization': self.producer})

        res = self.client().get('/movies/1',
                                headers={'Authorization': self.producer})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_get_one_movie(self):
        """Test getting non existing movie"""
        res = self.client().get('/movies/1',
                                headers={'Authorization': self.producer})

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
