import os
from flask import Flask
from skincare_package import app

if os.path.exists("env.py"):
    import env

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
