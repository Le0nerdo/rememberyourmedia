from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

import routes.misc_routes  # noqa: E402, F401
import routes.users_routes  # noqa: E402, F401
import routes.notes_routes  # noqa: E402, F401
import routes.friends_routes  # noqa: E402, F401
