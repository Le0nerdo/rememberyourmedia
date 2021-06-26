import typing

from db import db
from flask import session
# in friends for speed user1 = user and user2 = friend. All friendships have 2 entries.
# in friendrequests user1 = to be added and user2 = sender.


def get() -> typing.List[str]:
	sql = """
		SELECT users.username AS username
		FROM friends
		INNER JOIN users ON users.id=friends.user2
		WHERE friends.user1=:user
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
		INNER JOIN users ON users.id=friendrequests.user2
		WHERE friendrequests.user1=:user
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
			WHERE user1=:user AND user2=(SELECT id from friend)
			RETURNING user1, user2
		), link1 AS (
			INSERT INTO friends (user1, user2)
			VALUES ((SELECT user1 FROM request), (SELECT user2 FROM request))
			RETURNING user1, user2
		)
		INSERT INTO friends (user1, user2)
		VALUES ((SELECT user2 FROM request), (SELECT user1 FROM request))
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
		WHERE user1=:user AND user2=(SELECT id FROM friend)
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
		WHERE user2=:user AND user1=:friendid
		UNION
		SELECT id
		FROM friends
		WHERE user2=:user AND user1=:friendid
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
		INSERT INTO friendrequests (user1, user2)
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
			WHERE user1=:user AND user2=(SELECT id FROM friend)
		)
		DELETE
		FROM friends
		WHERE user1=(SELECT id FROM friend) AND user2=:user
	"""
	params = {"user": session["user_id"], "username": username}
	db.session.execute(sql, params)
	db.session.commit()
