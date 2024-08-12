from skincare_package import db
from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize the MongoDB client and select the database
client = MongoClient('mongodb://localhost:27017/')
db = client['Skincare_db']

# For collection: users
users_collection = db['users']

# Collection: users_routines
users_routines_collection = db['users_routines']

# Collection: skintype
skintype_collection = db['skintype']

