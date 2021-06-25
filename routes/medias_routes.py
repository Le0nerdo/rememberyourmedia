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
def edit(type: str, id: int):
	if type not in medias.TYPE_NAMES:
		return render_template("error.html")
	if "user_id" not in session:
		return redirect("/")
	if request.method == "GET":
		target = medias.get(type, id)
		if not target:
			return redirect("/")
		return render_template(f"/edit/{type}.html", media=target, type=type)
	if not users.valid():
		return render_template("error.html")
	name = request.form["name"]
	shared = request.form["shared"]
	if shared not in ["0", "1"]:
		return render_template("error.html")
	if len(name) < 1 or len(name) > 255:
		media = {"id": id}
		return render_template(
			f"/edit/{type}.html",
			type=type,
			media=media,
			name=name,
			shared=shared,
			edited="true",
			error="Media name length has to be between 1 and 255 characters."
		)
	edited = medias.edit({"name": name}, shared, type, id)
	if edited:
		return render_template(f"/edit/{type}.html", media=edited, type=type)
	return redirect("/", error="Target media could not be found.")


@app.route("/delete/<type>/<int:id>", methods=["POST"])
def delete(type: str, id: int):
	if type not in medias.TYPE_NAMES:
		return render_template("error.html")
	if "user_id" not in session:
		return redirect("/")
	if not users.valid():
		return render_template("error.html")
	medias.delete(type, id)
	return redirect("/browse")
