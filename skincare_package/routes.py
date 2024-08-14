from flask import render_template, request, redirect, url_for, flash, session, Flask
from skincare_package import app, mongo

@app.route('/')
def home():
    return render_template('home.html')


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
