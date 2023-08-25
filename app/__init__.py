# import os
# from flask import Flask
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
# basedir = os.path.abspath(os.path.dirname(__file__))
# app = Flask(__name__)
# app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "hangman.db"
# )
# app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DATABASE_URL = "postgresql://user:12345@hangman_database:5432/postgres"
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.app_context().push()
db.create_all()

from app.models.account_model import Account

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return Account.query.get(int(user_id))


from app import routes
