import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from skincare_package import app, models
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Load MongoDB URI from environment variable
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
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
        username = request.form.get("username").lower()
        print(f"Attempting login for user: {username}")

        existing_user = mongo.db.users.find_one({"username": username})

        if existing_user:
            print("User found in database")
            print(f"Stored hash: {existing_user['password']}")  # Debugging

            if check_password_hash(
                existing_user["password"], request.form.get("password")
            ):
                print("Password check passed")
                session["user"] = username

                # Retrieve and store user skin type in the session
                user_skintype = mongo.db.user_skintype.find_one(
                    {"username": session["user"]}
                )
                session["user_skintype"] = (
                    user_skintype.get("skin_type") if user_skintype else None
                )

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

        hashed_password = generate_password_hash(password)
        print(f"Registering user: {username}")

        register = {"username": username, "password": hashed_password}
        mongo.db.users.insert_one(register)

        session["user"] = username
        flash("Registration Successful!")
        return redirect(url_for("profile_skintype", username=session["user"]))

    return render_template("register.html")


@app.route('/profile_skintype', methods=["GET", "POST"])
def profile_skintype():
    if request.method == "POST":
        selected_skin_type = request.form.get('group1')

        if "user" in session:
            username = session["user"]

            try:
                # Update the user's skin type in the database
                mongo.db.user_skintype.update_one(
                    {"username": username},
                    {"$set": {"skin_type": selected_skin_type}},
                    upsert=True
                )

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
        updated_data = {
            "skincare_step": request.form.get("skincare_step"),
            "product_name": request.form.get("product_name"),
            "time_of_day": request.form.get("time_of_day"),
            "updated_at": datetime.utcnow()
        }

        mongo.db.skincare_entries.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": updated_data}
        )
        flash("Skincare entry updated successfully!")
        return redirect(url_for('profile_routine'))

    entry = mongo.db.skincare_entries.find_one({"_id": ObjectId(entry_id)})
    return render_template("edit_entry.html", entry=entry)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        selected_skin_type = request.form.get('skincare_step')
        product_name = request.form.get('product_name')
        time_of_day = request.form.get('time_of_day')

        if "user" in session:
            username = session["user"]
            print("Username from session:", username)  # Debugging

            try:
                result = mongo.db.skincare_entries.insert_one({
                    "username": username,
                    "skincare_step": selected_skin_type,
                    "product_name": product_name,
                    "time_of_day": time_of_day,
                    "created_at": datetime.utcnow()
                })
                flash("Skincare entry saved successfully!", "success")
            except Exception as e:
                print(f"Error inserting skincare entry: {e}")
                flash("An error occurred", "error")

            return redirect(url_for('profile'))
        else:
            flash("Please log in to save your skincare entry.", "error")
            return redirect(url_for('login'))

    else:
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
        entries = list(mongo.db.skincare_entries.find({"username": username}))

        entries_by_date = defaultdict(list)
        for entry in entries:
            entry_date = entry['created_at'].date()
            entries_by_date[entry_date].append(entry)

        entries_by_date = dict(sorted(entries_by_date.items(), reverse=True))

    else:
        entries_by_date = {}

    return render_template(
        "profile_routine.html", entries_by_date=entries_by_date)


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
    if 'user_skintype' in session:
        skin_type = session['user_skintype']
        products = list(mongo.db.products.find({"skin_type": skin_type}))
        return render_template("products.html", products=products)
    else:
        flash("Please set your skin type to get product recommendations.")
        return redirect(url_for('profile_skintype'))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False # turned off prior to final deployment
    )
