import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from skincare_package import app, models
from datetime import datetime


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


def jls_extract_def():
    
    return 


@app.route('/profile_skintype', methods=["GET", "POST"])
def profile_skintype():
    if request.method == "POST":
        # Get the selected skin type from the form
        selected_skin_type = request.form.get('group1')

        # Check if the user is logged in
        if "user" in session:
            username = session["user"]

            # Update the user's skin type in the database
            mongo.db.user_skintype.update_one(
                {"username": username},
                {"$set": {"skin_type": selected_skin_type}},
                upsert=True
            )
            flash("Skin type updated successfully!")
            return redirect(url_for('profile'))  # Redirect to the same page or another page as needed
        else:
            flash("Please log in to update your skin type.")
            return redirect(url_for('login'))  # Redirect to login if the user is not logged in

    # Render the profile skintype form
    return render_template("profile_skintype.html")

# Profile page where users can add entries 
@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        # Get the selected skincare step, product name, and time of day from the form
        selected_skin_type = request.form.get('skincare_step')
        product_name = request.form.get('product_name')
        time_of_day = request.form.get('time_of_day')

        # Check if the user is logged in
        if "user" in session:
            username = session["user"]

            # Save the skincare data into the MongoDB collection
            mongo.db.skincare_entries.insert_one({
                "username": username,
                "skincare_step": selected_skin_type,
                "product_name": product_name,
                "time_of_day": time_of_day,
                "created_at": datetime.utcnow()  # Store the timestamp of the entry
            })

            flash("Skincare entry saved successfully!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Please log in to save your skincare entry.", "error")
            return redirect(url_for('login'))

    return render_template("profile.html")


@app.route('/profile_routine', methods=["GET", "POST"])
def profile_routine():
    if "user" in session:
        username = session["user"]
        # Retrieve all skincare entries for the logged-in user
        entries = list(mongo.db.skincare_entries.find({"username": username}))
    else:
        # If the user is not logged in, initialize entries as an empty list
        entries = []

    return render_template("profile_routine.html", entries=entries)


@app.route('/logout')
def logout():
    session.clear()

    flash("You have been logged out successfully.", "info")

    return redirect(url_for('home'))


@app.route('/delete_entry/<entry_id>', methods=["POST"])
def delete_entry(entry_id):
    if "user" in session:
        username = session["user"]

        result = mongo.db.skincare_entries.delete_one({
            "_id": ObjectId(entry_id), 
            "username": username
        })

        if result.deleted_count > 0:
            flash("Entry deleted successfully!", "success")
        else:
            flash("Entry not found or not authorized to delete.", "error")
    else:
        flash("You need to be logged in to delete an entry.", "error")

    return redirect(url_for('profile_routine'))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
