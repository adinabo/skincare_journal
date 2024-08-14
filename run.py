import os
from flask import Flask, render_template
from skincare_package import app, models

app = Flask(__name__)

if os.path.exists("env.py"):
    import env

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = mongo.db.users.find_one({"username": username})
        
        if user and user["password"] == password:
            session["user"] = username
            return redirect(url_for("profile"))
        else:
            flash("Login failed. Please check your username and password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])  # Added the missing route decorator
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        existing_user = mongo.db.users.find_one({"username": username})
        
        if existing_user:
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("register"))
        
        mongo.db.users.insert_one({"username": username, "password": password})
        session["user"] = username
        return redirect(url_for("profile"))

    return render_template("register.html")

#def seed_database():
    # Check if users collection is empty
#    if models.users_collection.count_documents({}) == 0:
#        print("Seeding initial data...")

        # Create a new user
#        user_id = models.create_user("john_doe", "john@example.com", "hashed_password").inserted_id

        # Create a new skin type
#        skin_type_id = models.create_skin_type(
 #           "oily",
#            "Skin produces excess sebum, often with enlarged pores and a shiny appearance.",
 #           ["acne", "blackheads", "oily T-zone"],
 #           ["oil-free cleansers", "mattifying moisturizers"]
 #       ).inserted_id

        # Create a new routine for the user
#        models.create_user_routine(
 #           user_id,
 #           skin_type_id,
#            "Cleanser: CeraVe Hydrating Cleanser: Removes makeup and impurities without stripping the skin."
#        )

#        print("User and routine created successfully")
#    else:
 #       print("Data already exists in the database. Skipping seeding.")

#seed_database()

if __name__ == "__main__":
    # Run the Flask application
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
