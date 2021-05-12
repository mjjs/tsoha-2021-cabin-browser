from flask import Flask, g
from flask_login import LoginManager
from uuid import uuid4
from user import User, UserRole
from config import FLASK_SECRET_KEY
from db import get_db

from login import login_routes
from register import register_routes

app = Flask(__name__)
app.register_blueprint(login_routes)
app.register_blueprint(register_routes)
app.secret_key = FLASK_SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db:
        db.close()

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        db = get_db()
        return db.user_repository.get_user_by_id(user_id)

@app.route("/", methods = ["GET"])
def login_get():
    return "HELLO WORLD"

def main():
    app.run(debug = True)

if __name__ == "__main__":
    main()
