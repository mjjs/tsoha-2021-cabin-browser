from flask import Flask, g, redirect, render_template
from flask_login import LoginManager
from werkzeug.exceptions import RequestEntityTooLarge
from config import FLASK_SECRET_KEY, UPLOAD_FOLDER, ENVIRONMENT, PORT, MAX_CONTENT_LENGTH
from db import get_db

from login_routes import login_routes
from logout_routes import logout_routes
from register_routes import register_routes
from cabin_routes import cabin_routes
from keyword_routes import keyword_routes
from reservation_routes import reservation_routes
from review_routes import review_routes

app = Flask(__name__)
app.register_blueprint(login_routes)
app.register_blueprint(logout_routes)
app.register_blueprint(register_routes)
app.register_blueprint(cabin_routes)
app.register_blueprint(keyword_routes)
app.register_blueprint(reservation_routes)
app.register_blueprint(review_routes)
app.secret_key = FLASK_SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

login_manager = LoginManager()
login_manager.login_view = "login_routes.login_get"
login_manager.init_app(app)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db:
        db.close()

@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def handle_too_large_files(e):
    return render_template("too_large_file.html")

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        db = get_db()
        return db.user_repository.get(user_id)

@app.route("/", methods = ["GET"])
def index_get():
    return redirect("/cabins")

def main():
    app.run(
            debug = ENVIRONMENT == "DEV",
            host = "0.0.0.0",
            port = PORT,
            )

if __name__ == "__main__":
    main()
