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

app = Flask(__name__)
app.template_folder = 'templates'

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") 
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

def index():
    if mongo.db:
        return "Database connected"
    else:
        return "Database not connected", 500


app.route("/")
def home():
    return render_template("home.html") 

#@app.route("/users_routines")
#def users_routines():
#    users_routines = mongo.db.users_routines.find()
#    return render_template("routines.html", users_routines=users_routines)
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Check if the user already exists
        existing_user = mongo.db.users.find_one({'username': username})

        if existing_user:
            flash('Username already exists, please log in')
            return redirect(url_for('register'))

        # Hash the password and insert the new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({'username': username, 'password': hashed_password})
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form.get('username').lower()
        password = request.form.get('password')

        # Find the user by username
        user = mongo.db.users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = user['username']
            flash('Login successful!')
            return redirect(url_for('journal'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if 'user' in session:
        username = session['user']

        if request.method == 'POST':
            entry_content = request.form.get('content')
            mongo.db.journal.insert_one({
                'username': username,
                'content': entry_content,
                'timestamp': datetime.datetime.now()
            })
            flash('Journal entry added!')

        # Retrieve all journal entries for the logged-in user
        entries = mongo.db.journal.find({'username': username})

        return render_template('journal.html', entries=entries)

    flash('Please log in to access your journal')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

