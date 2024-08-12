import os
from flask import Flask, render_template
from skincare_package import app

app = Flask(__name__)

if os.path.exists("env.py"):
    import env

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
