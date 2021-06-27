import typing

from db import db
from flask import session


def get() -> typing.List[str]:
	sql = """
		SELECT users.username AS username
		FROM friends
		INNER JOIN users ON users.id=friends.friend
		WHERE friends.user=:user
	"""
	params = {"user": session["user_id"]}
	result = db.session.execute(sql, params)
	rows = result.fetchall()
	print("WTF", rows)
	return [row.username for row in rows]


def friend_requests():
	sql = """
		SELECT users.username AS username
		FROM friendrequests
		INNER JOIN users ON users.id=friendrequests.sender
		WHERE friendrequests.receiver=:user
	"""
	params = {"user": session["user_id"]}
	result = db.session.execute(sql, params)
	rows = result.fetchall()
	return [row.username for row in rows]


def accept_friend_request(username: str):
	sql = """
		WITH friend AS (
			SELECT id
			FROM users
			WHERE username=:username
		), request AS (
			DELETE
			FROM friendrequests
			WHERE receiver=:user AND sender=(SELECT id from friend)
			RETURNING receiver, sender
		), link1 AS (
			INSERT INTO friends ("user", friend)
			VALUES (:user, (SELECT id from friend))
			RETURNING "user", friend
		)
		INSERT INTO friends ("user", friend)
		VALUES ((SELECT id from friend), :user)
	"""
	params = {"user": session["user_id"], "username": username}
	db.session.execute(sql, params)
	db.session.commit()
	return


def decline_friend_request(username: str):
	sql = """
		WITH friend AS (
			SELECT id
			FROM users
			WHERE username=:username
		)
		DELETE
		FROM friendrequests
		WHERE receiver=:user AND sender=(SELECT id FROM friend)
	"""
	params = {"user": session["user_id"], "username": username}
	db.session.execute(sql, params)
	db.session.commit()


def send_friend_request(username: str) -> int:
	"""
	Returns 0 if send friend request,
	1 if accepted friend request,
	2 if friendrequest already send or are friends
	3 if user not found
	"""
	if username == session["username"]:
		return 2
	sql_get_user = "SELECT id FROM users WHERE username=:username"
	friend = db.session.execute(sql_get_user, {"username": username}).fetchone()
	if not friend:
		return 3
	sql_check_exist = """
		SELECT id
		FROM friendrequests
		WHERE sender=:user AND receiver=:friendid
		UNION
		SELECT friend
		FROM friends
		WHERE "user"=:user AND friend=:friendid
	"""
	params = {"user": session["user_id"], "friendid": friend.id}
	exists = db.session.execute(sql_check_exist, params).fetchall()
	print("BITSADF", exists)
	if exists:
		return 2
	if username in friend_requests():
		accept_friend_request(username)
		return 1
	sql_insert_friendrequest = """
		INSERT INTO friendrequests (receiver, sender)
		VALUES (:friendid, :user)
	"""
	db.session.execute(sql_insert_friendrequest, params)
	db.session.commit()
	return 0


def remove_friend(username: str):
	sql = """
		WITH friend AS (
			SELECT id
			FROM users
			WHERE username=:username
		), link1 AS (
			DELETE
			FROM friends
			WHERE "user"=:user AND friend=(SELECT id FROM friend)
		)
		DELETE
		FROM friends
		WHERE "user"=(SELECT id FROM friend) AND friend=:user
	"""
	params = {"user": session["user_id"], "username": username}
	db.session.execute(sql, params)
	db.session.commit()
