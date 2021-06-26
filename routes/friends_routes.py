from app import app
from flask import redirect, render_template, request, session
import handlers.friends as friends
import handlers.users as users


@app.route("/friends", methods=["GET"])
def friends_overview():
	if "user_id" not in session:
		return redirect("/")
	requests = friends.friend_requests()
	current = friends.get()
	return render_template("friends.html", requests=requests, friends=current)


@app.route("/friends/add", methods=["POST"])
def add_friend():
	if "user_id" not in session:
		return redirect("/")
	if not users.valid():
		return render_template("error.html")
	username = request.form["username"]
	status = friends.send_friend_request(username)
	if status == 0 or status == 1:
		return redirect("/friends")
	requests = friends.friend_requests()
	current = friends.get()
	if status == 2:
		return render_template(
			"friends.html",
			requests=requests,
			friends=current,
			error="Already friends or request already sent."
		)
	if status == 3:
		return render_template(
			"friends.html",
			requests=requests,
			friends=current,
			error=f"User '{username}' could not be found."
		)
	return render_template("error.html")


@app.route("/friends/accept", methods=["POST"])
def accept_friend():
	if "user_id" not in session:
		return redirect("/")
	if not users.valid():
		return render_template("error.html")
	username = request.form["username"]
	friends.accept_friend_request(username)
	return redirect("/friends")


@app.route("/friends/decline", methods=["POST"])
def decline_friend():
	if "user_id" not in session:
		return redirect("/")
	if not users.valid():
		return render_template("error.html")
	username = request.form["username"]
	friends.decline_friend_request(username)
	return redirect("/friends")


@app.route("/friends/remove", methods=["POST"])
def remove_friend():
	if "user_id" not in session:
		return redirect("/")
	if not users.valid():
		return render_template("error.html")
	username = request.form["username"]
	friends.remove_friend(username)
	return redirect("/friends")
