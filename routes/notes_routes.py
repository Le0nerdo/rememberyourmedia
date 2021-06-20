from app import app
from flask import redirect, render_template, request, session
import handlers.users as users
import handlers.medias as medias


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
	if len(name) < 1 or len(name) > 255:
		return render_template(
			"create.html",
			type=type,
			name=name,
			shared=shared,
			error="Media name length has to be between 1 and 255 characters."
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
