import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from skincare_package import app, models

app = Flask(__name__)

# Load MongoDB URI from environment variable
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

# Print the MongoDB URI to verify it's being loaded correctly 
print(f"Mongo URI: {os.getenv('MONGO_URI')}")


if os.path.exists("env.py"):
    import env


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# Check if the MongoDB connection is successful
if mongo.db is None:
    print("Failed to initialize MongoDB connection!")
else:
    print("MongoDB connection initialized successfully!")


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile_skintype", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()}) 

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile_skintype", username=session["user"]))

    return render_template("register.html")


@app.route('/profile_skintype', methods=["GET", "POST"])
def profile_skintype():
    if "user" in session:
        username = session["user"]
        return render_template("profile_skintype.html", username=username)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    # Run the Flask application
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
