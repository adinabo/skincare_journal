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

@app.route('/profile')
def profile():
    if "user" in session:
        username = session["user"]
        return render_template("profile.html", username=username)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    # Run the Flask application
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
