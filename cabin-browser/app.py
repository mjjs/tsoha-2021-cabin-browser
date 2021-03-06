from flask import Flask, redirect, render_template
from flask_login import LoginManager
from flask_seasurf import SeaSurf
from werkzeug.exceptions import RequestEntityTooLarge
from config import (
    FLASK_SECRET_KEY,
    UPLOAD_FOLDER,
    ENVIRONMENT,
    PORT,
    MAX_CONTENT_LENGTH,
)
from user import UserRepository, user_routes
from db import connection_pool
from waitress import serve

from cabin import cabin_routes
from keywords import keyword_routes
from reservation import reservation_routes
from review import review_routes

app = Flask(__name__)
app.register_blueprint(user_routes)
app.register_blueprint(cabin_routes)
app.register_blueprint(keyword_routes)
app.register_blueprint(reservation_routes)
app.register_blueprint(review_routes)
app.secret_key = FLASK_SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

login_manager = LoginManager()
login_manager.login_view = "user_routes.login_get"
login_manager.init_app(app)

csrf = SeaSurf()
csrf.init_app(app)


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def handle_too_large_files(e):
    return render_template("too_large_file.html")


@login_manager.user_loader
def load_user(user_id):
    return UserRepository(connection_pool).get(user_id)


@app.route("/", methods=["GET"])
def index_get():
    return redirect("/cabins")


def main():
    serve(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
