import typing

from db import db
from flask import session, request
from werkzeug.security import check_password_hash, generate_password_hash
import secrets


def login(username: str, password: str) -> bool:
	sql: str = "SELECT password_hash, id FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username": username})
	user = result.fetchone()
	if user is None:
		return False
	else:
		if check_password_hash(user[0], password):
			session["user_id"] = user[1]
			session["username"] = username
			session["csrf_token"] = secrets.token_hex(16)
			return True
		else:
			return False


def logout() -> None:
	del session["user_id"]
	del session["username"]
	del session["csrf_token"]


def register(username: str, email: str, password: str) -> bool:
	hash_value = generate_password_hash(password)
	try:
		sql: str = (
			"INSERT INTO users (username,email,password_hash)"
			"VALUES (:username,:email,:password_hash)"
		)
		db.session.execute(sql, {"username": username, "email": email, "password_hash": hash_value})
		db.session.commit()
	except Exception:
		return False
	return login(username, password)


def check_availability(username: str, email: str) -> typing.Tuple[bool, bool]:
	sql: str = "SELECT username, email FROM users WHERE (username=:username OR email=:email)"
	result = db.session.execute(sql, {"username": username, "email": email})
	found = result.fetchall()
	username_available: bool = True
	email_available: bool = True
	for user, mail in found:
		if user == username:
			username_available = False
		if mail == email:
			email_available = False
	return (username_available, email_available)


def user_id() -> int:
	return session.get("user_id", 0)


def valid() -> bool:
	if "user_id" not in session:
		return False
	if session["csrf_token"] != request.form["csrf_token"]:
		return False
	return True
