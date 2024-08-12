from flask import render_template, request, redirect, url_for, flash, session, Flask
from skincare_package import app, mongo

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

@app.route('/profile')
def profile():
    if "user" in session:
        username = session["user"]
        return render_template("profile.html", username=username)
    else:
        return redirect(url_for("login"))

@app.route("/routine")
def routine():
    routine_list = list(mongo.db.users_routines.find())
    return render_template("routine.html", routines=routine_list)

@app.route("/add_routine", methods=["GET", "POST"])
def add_routine():
    if request.method == "POST":
        routine = {
            "routine_name": request.form.get("routine_name"),
            "description": request.form.get("description"),
            "skin_type_id": request.form.get("skin_type_id")
        }
        mongo.db.users_routines.insert_one(routine)
        return redirect(url_for("routine"))

    skin_types = list(mongo.db.skin_type.find())
    return render_template("add_routine.html", skin_types=skin_types)

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))
