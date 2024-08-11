from pymongo import MongoClient
import os


mongo_uri = "URI"

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()  
    print("Database connected successfully")
except Exception as e:
    print(f"An error occurred: {e}")
