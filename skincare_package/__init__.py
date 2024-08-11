import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

if os.path.exists("env.py"):
    import env
    
app = Flask(__name__)

# Configuration for MongoDB
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

