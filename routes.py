from app import app
from flask import redirect, render_template, request, session
import users
import medias


@app.route("/")
def index():
	return render_template("index.html")


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
			emai=email,
			error="Given passwords do not match."
		)
	if len(username) > 20:
		return render_template(
			"register.html",
			username=username,
			emai=email,
			error="Username can not be longer than 20 characters."
		)
	if len(email) > 255:
		return render_template(
			"register.html",
			username=username,
			emai=email,
			error="E-mail can not be longer than 255 characters."
		)
	if len(password) > 255:
		return render_template(
			"register.html",
			username=username,
			emai=email,
			error="Password can not be longer than 255 characters."
		)
	username_available, email_available = users.check_availability(username, email)
	if not username_available:
		return render_template(
			"register.html",
			username=username,
			emai=email,
			error="Username is already taken."
		)
	if not email_available:
		return render_template(
			"register.html",
			username=username,
			emai=email,
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


@app.route("/browse", methods=["GET", "POST"])
def browse():
	if "user_id" not in session:
		return redirect("/")
	if request.method == "GET":
		return render_template("browse.html", type="5")
	if not users.valid():
		return render_template("error.html")
	type = request.form["type"]
	pattern = request.form["pattern"]
	if type not in medias.TYPES:
		return render_template("error.html")
	if len(pattern) > 255:
		return render_template(
			"browse.html",
			type="5",
			error="Gave longer part for name than possible name length."
		)
	mediadata = medias.browse(pattern, type)
	return render_template(
		"browse.html",
		type=type,
		mediadata=mediadata,
		mediatemplate=medias.TEMPLATES[type]
	)


@app.route("/create", methods=["GET", "POST"])
def create():
	if "user_id" not in session:
		return redirect("/")
	if request.method == "GET":
		return render_template("create.html", type="5")
	if not users.valid():
		return render_template("error.html")
	type = request.form["type"]
	name = request.form["name"]
	shared = request.form["shared"]
	if (type not in medias.TYPES) or (shared not in ["0", "1"]):
		return render_template("error.html")
	if len(name) > 255:
		return render_template(
			"create.html",
			type=type,
			name=name,
			shared=shared,
			error="Media name can not be longer than 255 characters."
		)
	medias.create({"name": name}, shared, type)
	return render_template("create.html", type=type, shared=shared)


@app.route("/edit/<type>/<int:id>", methods=["GET", "POST"])
def edit(type: str, id: int):  # TODO
	if type not in medias.TYPE_NAMES:
		return render_template("error.html")
	if request.method == "GET":
		target = medias.get(type, id)
		if not target:
			return redirect("/")
		helper = "" if target.shared else "not "
		return f"Selected {target.name} with id {target.id} that is {helper}shared."  # TODO
	return redirect("/")  # TODO


@app.route("/friends")
def friends():
	return render_template("friends.html")
