from datetime import timedelta

from flask import Flask
from flask_wtf import CSRFProtect

from .database import db
from .environment import SESSION_SECRET

# csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.secret_key = SESSION_SECRET
    app.permanent_session_lifetime = timedelta(days=7)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)
    # csrf.init_app(app)

    with app.app_context():
        db.create_all()

    return app
