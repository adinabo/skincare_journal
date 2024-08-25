import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from skincare_package import app, models
from collections import defaultdict
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


# To check if the MongoDB connection is successful
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
        username = request.form.get("username").lower()
        print(f"Attempting login for user: {username}")

        # Check if username exists in db
        existing_user = mongo.db.users.find_one({"username": username})

        if existing_user:
            print("User found in database")

            # Debugging: Check password hash stored in database
            print(f"Stored hash: {existing_user['password']}")

            # Ensure hashed password matches user input
            if check_password_hash(existing_user["password"], request.form.get("password")):
                print("Password check passed")
                session["user"] = username

                # Retrieve and store user skin type in the session
                user_skintype = mongo.db.user_skintype.find_one({"username": session["user"]})
                if user_skintype:
                    session["user_skintype"] = user_skintype.get("skin_type")
                else:
                    session["user_skintype"] = None  # Handle case where no skin type is set

                flash("Welcome, {}".format(username))
                return redirect(url_for("profile_skintype"))
            else:
                print("Password check failed")
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            print("User not found in database")
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        
        # Check if username already exists in db
        existing_user = mongo.db.users.find_one({"username": username}) 

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Hash the password
        hashed_password = generate_password_hash(password)
        print(f"Registering user: {username} with hashed password: {hashed_password}")

        register = {
            "username": username,
            "password": hashed_password
        }
        mongo.db.users.insert_one(register)

        # Put the new user into 'session' cookie
        session["user"] = username
        flash("Registration Successful!")
        return redirect(url_for("profile_skintype", username=session["user"]))

    return render_template("register.html")


def jls_extract_def():
    
    return 


@app.route('/profile_skintype', methods=["GET", "POST"])
def profile_skintype():
    if request.method == "POST":
        selected_skin_type = request.form.get('group1')

        # Check if the user is logged in
        if "user" in session:
            username = session["user"]

            try:
                # Update the user's skin type in the database
                mongo.db.user_skintype.update_one(
                    {"username": username},
                    {"$set": {"skin_type": selected_skin_type}},
                    upsert=True
                )
                
                # Update session variable to show new skin type
                session["user_skintype"] = selected_skin_type

                flash("Skin type updated successfully!")
            except Exception as e:
                print(f"Error updating skin type: {e}")
                flash("An error occurred while updating your skin type.")
            
            return redirect(url_for('profile'))
        else:
            flash("Please log in to update your skin type.")
            return redirect(url_for('login'))

    return render_template("profile_skintype.html")


@app.route('/edit_entry/<entry_id>', methods=["GET", "POST"])
def edit_entry(entry_id):
    if request.method == "POST":
        # Handle the form submission to update the entry
        updated_data = {
            "skincare_step": request.form.get("skincare_step"),
            "product_name": request.form.get("product_name"),
            "time_of_day": request.form.get("time_of_day"),
            "updated_at": datetime.utcnow()
        }
        # Update the entry in the database
        mongo.db.skincare_entries.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": updated_data}
        )
        flash("Skincare entry updated successfully!")
        return redirect(url_for('profile_routine'))

    # If GET request, render the edit form with existing data
    entry = mongo.db.skincare_entries.find_one({"_id": ObjectId(entry_id)})
    return render_template("edit_entry.html", entry=entry)


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
            print("Username from session:", username)  # Debugging

            try:
                # Save the skincare data into the MongoDB collection
                result = mongo.db.skincare_entries.insert_one({
                    "username": username,
                    "skincare_step": selected_skin_type,
                    "product_name": product_name,
                    "time_of_day": time_of_day,
                    "created_at": datetime.utcnow()  # Store the timestamp of the entry
                })
                flash("Skincare entry saved successfully!", "success")
            except Exception as e:
                print(f"Error inserting skincare entry: {e}")
                flash("An error occurred while saving your skincare entry.", "error")

            return redirect(url_for('profile'))
        else:
            flash("Please log in to save your skincare entry.", "error")
            return redirect(url_for('login'))

    else:
        # Fetch products based on the user's skin type and skincare step
        user_skin_type = session.get("user_skintype")
        products_by_step = {}

        if user_skin_type:
            skincare_steps = ["cleanser", "moisturizer", "serum", "peeling"]

            for step in skincare_steps:
                products_by_step[step] = list(mongo.db.products.find({
                    "type": step.capitalize(),
                    "skin_type": user_skin_type
                }))

    return render_template("profile.html", products=products_by_step)


@app.route('/profile_routine', methods=["GET", "POST"])
def profile_routine():
    if "user" in session:
        username = session["user"]
        # Retrieve all skincare entries for the logged-in user
        entries = list(mongo.db.skincare_entries.find({"username": username}))

        # Group entries by date (only date part, ignore time)
        entries_by_date = defaultdict(list)
        for entry in entries:
            entry_date = entry['created_at'].date()  # Get the date part
            entries_by_date[entry_date].append(entry)

        # Sort entries by date
        entries_by_date = dict(sorted(entries_by_date.items(), reverse=True))

    else:
        # If the user is not logged in, initialize entries_by_date as an empty dict
        entries_by_date = {}

    return render_template("profile_routine.html", entries_by_date=entries_by_date)


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


@app.route('/add_routine', methods=["POST"])
def add_routine():
    if "user" in session:
        username = session["user"]

        routine = [
            {
                "step_name": request.form.get("step_name1"),
                "product_used": request.form.get("product_used1"),
                "time_of_day": request.form.get("time_of_day1"),
            },
            {
                "step_name": request.form.get("step_name2"),
                "product_used": request.form.get("product_used2"),
                "time_of_day": request.form.get("time_of_day2"),
            }
        ]
        # Store the routine in the database
        mongo.db.routines.insert_one({
            "username": username,
            "routine": routine
        })
        flash("Routine added successfully!")
        return redirect(url_for('profile'))
    else:
        flash("Please log in to add a routine.")
        return redirect(url_for('login'))


@app.route('/products')
def products():
    # Check if the user is logged in and has a skin type set
    if 'user_skintype' in session:
        skin_type = session['user_skintype']
        
        # Query the database for products that match the user's skin type
        products = list(mongo.db.products.find({"skin_type": skin_type}))

        # Render the product recommendations page with the products
        return render_template("products.html", products=products)
    
    else:
        # If the user's skin type is not set, redirect them to set it first
        flash("Please set your skin type to get product recommendations.")
        return redirect(url_for('profile_skintype'))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
