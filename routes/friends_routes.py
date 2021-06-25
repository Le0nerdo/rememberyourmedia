from app import app
from flask import render_template


@app.route("/friends")
def friends():
	return render_template("friends.html")
