from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize the MongoDB client and select the database
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['Skincare_db']

# Collection: users
users_collection = db['users']

# Collection: skintype
skintype_collection = db['skintype']

# Collection: users_routines
users_routines_collection = db['users_routines']

# Create a new user
def create_user(username, email, password_hash):
    user = {
        "username": username,
        "email": email,
        "password": password_hash,
    }
    return users_collection.insert_one(user)

# Create a new skin type
def create_skin_type(skin_type, description, concerns, care_tips):
    skin_type_doc = {
        "_id": ObjectId(),
        "skin_type": skin_type,
        "description": description,
        "concerns": concerns,
        "care_tips": care_tips,
    }
    return skintype_collection.insert_one(skin_type_doc)

# Create a new routine for the user
def create_user_routine(user_id, skintype_id, routine):
    user_routine = {
        "_id": ObjectId(),
        "user_id": ObjectId(user_id),
        "skintype_id": ObjectId(skintype_id),
        "routine": routine,
    }
    return users_routines_collection.insert_one(user_routine)

# Retrieving all users
def get_all_users():
    return list(users_collection.find())

# retrieving routines for a user
def get_user_routines(user_id):
    return list(users_routines_collection.find({"user_id": ObjectId(user_id)}))
