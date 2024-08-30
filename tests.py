from pymongo import MongoClient
import unittest
from flask import Flask
from flask_pymongo import PyMongo
import os
from env import *

mongo_uri = "URI"


class MongoConnectionTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        # Use the MongoDB URI from environment variables
        self.app.config["MONGO_URI"] = os.getenv("MONGO_URI")
        self.mongo = PyMongo(self.app)

    def test_mongo_connection(self):
        with self.app.app_context():
            try:
                # Test connection with a ping command
                self.mongo.cx.admin.command('ping')
                print("MongoDB connection is successful!")
            except Exception as e:
                self.fail(f"MongoDB connection failed: {e}")


if __name__ == '__main__':
    unittest.main()
