import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for
)
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from skincare_package import routes

if os.path.exists("env.py"):
    import env
