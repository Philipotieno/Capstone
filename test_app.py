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
        
        self.actor = {
            "name" : "test actor",
            "age" : 12,
            "gender" : "male"
        }
        
        self.movie = {
            "name" : "test actor",
            "age" : 12,
            "gender" : "male"
        }
        
        # Binds the app to the current context
        with self.app.app_context():
            db.create_all()
    
    def test_endpoint(self):
        res = self.client().get('/')
        self.assertIn('There are no actors', str(res.data),)
    
    def tearDown(self):
        pass
    
if __name__ == "__main__":
    unittest.main()