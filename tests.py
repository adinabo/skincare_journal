from pymongo import MongoClient
import unittest
from flask import Flask
from flask_pymongo import PyMongo
import os


mongo_uri = "URI"

#try:
#    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
#    client.server_info()  
#    print("Database connected successfully")
#except Exception as e:
#    print(f"An error occurred: {e}")


from env import *


class MongoConnectionTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        # Use the MongoDB URI from environment variables
        self.app.config["MONGO_URI"] = os.getenv("MONGO_URI")
        self.mongo = PyMongo(self.app)

    def test_mongo_connection(self):
        with self.app.app_context():
            try:
                # Test connection with a simple ping command
                self.mongo.cx.admin.command('ping')
                print("MongoDB connection is successful!")
            except Exception as e:
                self.fail(f"MongoDB connection failed: {e}")

if __name__ == '__main__':
    unittest.main()