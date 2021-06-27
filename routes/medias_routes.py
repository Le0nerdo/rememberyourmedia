from app import app
from flask import redirect, render_template, request, session
import handlers.users as users
import handlers.medias as medias


@app.route("/browse", methods=["GET"])
def browse():
	if "user_id" not in session:
		return redirect("/")
	return render_template("browse.html")


@app.route("/browse/<m_type>", methods=["GET", "POST"])
def browse_type(m_type: str):
	if "user_id" not in session:
		return redirect("/")
	if m_type not in medias.TYPE_NAMES:
		return redirect("/browse")
	if request.method == "GET":
		return render_template("browse.html", type=m_type)
	if not users.valid():
		return render_template("error.html")
	pattern = request.form["pattern"]
	if len(pattern) > 255:
		return render_template(
			"browse.html",
			type="5",
			error="Gave longer part for name than possible name length."
		)
	mediadata = medias.browse(pattern, m_type)
	shared_data = medias.browse_friends(pattern, m_type)
	return render_template(
		"browse.html",
		type=m_type,
		mediadata=[dict(m) for m in mediadata],
		shared_data=[dict(m) for m in shared_data]
	)


@app.route("/create", methods=["GET"])
def create():
	if "user_id" not in session:
		return redirect("/")
	return render_template("create.html")


@app.route("/create/<m_type>", methods=["GET", "POST"])
def create_type(m_type: str):
	if "user_id" not in session:
		return redirect("/")
	if m_type not in medias.TYPE_NAMES:
		return redirect("/create")
	if request.method == "GET":
		return render_template("create.html", type=m_type, fields=medias.FIELDS[m_type])
	if not users.valid():
		return render_template("error.html")
	fields = medias.FIELDS[m_type]
	new_media = {}
	for field in fields:
		value = request.form[field["name"]]
		new_media[field["name"]] = value
	for field in fields:
		if not new_media[field["name"]] and not field["required"]:
			continue
		value = new_media[field["name"]]
		if field["type"] == "text":
			if not field["min"] <= len(value) or not field["max"] >= len(value):
				return render_template(
					"create.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					error=f"Length of {field['name']} has to be between {field['min']} and {field['max']}."
				)
		elif field["type"] == "number":
			try:
				as_number = int(float(value))
			except ValueError:
				return render_template(
					"create.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					error=f"{field['name']} has to be an integer between {field['min']} and {field['max']}."
				)
			if not field["min"] <= as_number or not field["max"] >= as_number:
				return render_template(
					"create.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					error=f"{field['name']} has to be an integer between {field['min']} and {field['max']}."
				)
		elif field["type"] == "checkbox":
			if value not in ["0", "1"]:
				return render_template("error.html")
	medias.create(new_media, type=m_type)
	return render_template(
		"create.html",
		type=m_type,
		fields=medias.FIELDS[m_type],
		message=f"Created {m_type} item with the Title {request.form['Title']}"
	)


@app.route("/edit/<m_type>/<int:id>", methods=["GET", "POST"])
def edit(m_type: str, id: int):
	if m_type not in medias.TYPE_NAMES:
		return render_template("error.html")
	if "user_id" not in session:
		return redirect("/")
	if request.method == "GET":
		target = medias.get(m_type, id)
		if not target:
			return redirect("/")
		fields = medias.fill_values_from_row(target, m_type)
		return render_template("edit.html", fields=fields, type=m_type, id=id)
	if not users.valid():
		return render_template("error.html")
	fields = medias.FIELDS[m_type]
	new_media = {}
	for field in fields:
		value = request.form[field["name"]]
		new_media[field["name"]] = value
	for field in fields:
		if not new_media[field["name"]] and not field["required"]:
			continue
		value = new_media[field["name"]]
		if field["type"] == "text":
			if not field["min"] <= len(value) or not field["max"] >= len(value):
				return render_template(
					"edit.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					id=id,
					error=f"Length of {field['name']} has to be between {field['min']} and {field['max']}."
				)
		elif field["type"] == "number":
			try:
				as_number = int(float(value))
			except ValueError:
				return render_template(
					"edit.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					id=id,
					error=f"{field['name']} has to be an integer between {field['min']} and {field['max']}."
				)
			if not field["min"] <= as_number or not field["max"] >= as_number:
				return render_template(
					"edit.html",
					type=m_type,
					fields=medias.fill_values_from_dict(new_media, m_type),
					id=id,
					error=f"{field['name']} has to be an integer between {field['min']} and {field['max']}."
				)
		elif field["type"] == "checkbox":
			if value not in ["0", "1"]:
				return render_template("error.html")
	new_row = medias.edit(new_media, m_type=m_type, id=id)
	if not new_row:
		return render_template(
			"edit.html",
			type=m_type,
			fields=medias.fill_values_from_dict(new_media, m_type),
			id=id,
			error="Media not found."
		)
	return render_template(
		"edit.html",
		type=m_type,
		fields=medias.fill_values_from_row(new_row, m_type),
		id=id,
		message="Saved changes"
	)


@app.route("/delete/<m_type>/<int:id>", methods=["GET", "POST"])
def delete(m_type: str, id: int):
	if m_type not in medias.TYPE_NAMES:
		return render_template("error.html")
	if "user_id" not in session:
		return redirect("/")
	if request.method == "GET":
		target = medias.get(m_type, id)
		if not target:
			return redirect("/")
		return render_template("delete.html", title=target.title, type=m_type, id=id)
	if not users.valid():
		return render_template("error.html")
	medias.delete(m_type, id)
	return redirect(f"/browse/{m_type}")
