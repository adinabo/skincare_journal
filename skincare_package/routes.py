from flask import render_template, request, redirect, url_for
from skincare_package import app, db
from skincare_package.models import SkinType, users_routines

@app.route("/")
def home():
    tasks = list(users_routines.query.order_by(users_routines.id).all())
    return render_template("tasks.html", tasks=tasks)

@app.route("/routine")
def routine():
    routine_list = list(users_routines.query.order_by(users_routines.routine_name).all())
    return render_template("routine.html", routine=routine_list)

@app.route("/add_routine", methods=["GET", "POST"])
def add_routine():
    if request.method == "POST":
        routine = users_routines(
            routine_name=request.form.get("routine_name"),
            description=request.form.get("description"),
            skin_type_id=request.form.get("skin_type_id")  # Assuming a dropdown/select input for skin_type_id
        )
        db.session.add(routine)
        db.session.commit()
        return redirect(url_for("routine"))
    skin_types = SkinType.query.all()  # To populate a dropdown or similar in the form
    return render_template("add_routine.html", skin_types=skin_types)
