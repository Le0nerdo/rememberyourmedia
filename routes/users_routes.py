from app import app
from flask import redirect, render_template, request
import handlers.users as users


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	username = request.form["username"]
	password = request.form["password"]
	if users.login(username, password):
		return redirect("/")
	else:
		return render_template(
			"login.html",
			username=username,
			error="Invalid credentials."
		)


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	username = request.form["username"]
	email = request.form["email"]
	password = request.form["password"]
	password_check = request.form["password_check"]
	if not password == password_check:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="Given passwords do not match."
		)
	if len(username) < 3 or len(username) > 20:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="Username length has to be between 3 and 20 characters."
		)
	if len(email) < 5 or len(email) > 255:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="E-mail length has to be between 5 and 255 characters."
		)
	if len(password) < 12 or len(password) > 255:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="Password length has to be between 12 and 255 characters."
		)
	username_available, email_available = users.check_availability(username, email)
	if not username_available:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="Username is already taken."
		)
	if not email_available:
		return render_template(
			"register.html",
			username=username,
			email=email,
			error="E-mail is already used for another user."
		)
	if users.register(username, email, password):
		return redirect("/")
	else:
		return render_template("register.html", error="Unexpected error while registering user.")


@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")
