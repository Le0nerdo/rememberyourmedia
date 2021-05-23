from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	sql = "SELECT id, password_hash FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username": username})
	user = result.fetchone()
	if user == None:
		pass # TODO
	else:
		pwhash = user[1]
		if check_password_hash(pwhash, password):
			session["userid"] = user[0] # ?
			session["username"] = username
		else:
			pass # TODO
	return redirect("/")

@app.route("/logout")
def logout():
	del session["username"]
	return redirect("/")

@app.route("/createuser", methods=["POST"])
def createuser():
	username = request.form["username"]
	email = request.form["email"]
	password = request.form["password"]
	pwhash = generate_password_hash(password)
	sql = "INSERT INTO users (username,email,password_hash) VALUES (:username,:email,:password)"
	db.session.execute(sql, {"username": username, "email": email, "password": pwhash})
	db.session.commit()
	return redirect("/")
