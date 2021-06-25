import re
import typing

from db import db
from flask import session

Media = dict

TYPES = ["0", "1", "2", "3", "4", "5"]
TYPE_NAMES = ["film", "music", "book", "comic", "game", "other"]

TEMPLATES = {
	"0": "media/film.html",
	"1": "media/music.html",
	"2": "media/book.html",
	"3": "media/comic.html",
	"4": "media/game.html",
	"5": "media/other.html"
}

FIELDS = {
	"0": ["name"],
	"1": ["name"],
	"2": ["name"],
	"3": ["name"],
	"4": ["name"],
	"5": ["name"]
}

SQL_BROWSE = {
	"0": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM films AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
	"1": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM music AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
	"2": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM books AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
	"3": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM comics AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
	"4": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM games AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
	"5": """
		SELECT m.name AS name, m.shared AS shared, u.username AS owner, m.id AS id
		FROM other AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.name ~* :pattern
	""",
}

SQL_INSERT = {
	"0": "INSERT INTO films (owner, name, shared) VALUES (:owner, :name, :shared)",
	"1": "INSERT INTO music (owner, name, shared) VALUES (:owner, :name, :shared)",
	"2": "INSERT INTO books (owner, name, shared) VALUES (:owner, :name, :shared)",
	"3": "INSERT INTO comics (owner, name, shared) VALUES (:owner, :name, :shared)",
	"4": "INSERT INTO games (owner, name, shared) VALUES (:owner, :name, :shared)",
	"5": "INSERT INTO other (owner, name, shared) VALUES (:owner, :name, :shared)"
}

SQL_GET = {
	"0": "SELECT * FROM films WHERE owner=:owner AND id=:id",
	"1": "SELECT * FROM music WHERE owner=:owner AND id=:id",
	"2": "SELECT * FROM books WHERE owner=:owner AND id=:id",
	"3": "SELECT * FROM comics WHERE owner=:owner AND id=:id",
	"4": "SELECT * FROM games WHERE owner=:owner AND id=:id",
	"5": "SELECT * FROM other WHERE owner=:owner AND id=:id",
}

SQL_EDIT = {
	"0": "UPDATE films SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
	"1": "UPDATE music SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
	"2": "UPDATE books SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
	"3": "UPDATE comics SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
	"4": "UPDATE games SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
	"5": "UPDATE other SET name=:name, shared=:shared WHERE owner=:owner AND id=:id RETURNING *;",
}

SQL_DELETE = {
	"0": "DELETE FROM films WHERE owner=:owner AND id=:id",
	"1": "DELETE FROM music WHERE owner=:owner AND id=:id",
	"2": "DELETE FROM books WHERE owner=:owner AND id=:id",
	"3": "DELETE FROM comics WHERE owner=:owner AND id=:id",
	"4": "DELETE FROM games WHERE owner=:owner AND id=:id",
	"5": "DELETE FROM other WHERE owner=:owner AND id=:id",
}


def browse(pattern: str, m_type: str) -> typing.List[Media]:
	result = db.session.execute(
		SQL_BROWSE[m_type],
		{"pattern": re.escape(pattern), "owner": session["user_id"]}
	)
	rows = result.fetchall()
	medias = []
	for row in rows:
		media = dict(row)
		media["type"] = TYPE_NAMES[int(m_type)]
		medias.append(media)
	return medias


def create(fields: dict, shared: str, type: int) -> None:
	params = {**fields, "owner": session["user_id"], "shared": shared}
	db.session.execute(SQL_INSERT[type], params)
	db.session.commit()


def get(m_type: str, id: int) -> Media:
	result = db.session.execute(
		SQL_GET[TYPES[TYPE_NAMES.index(m_type)]],
		{"owner": session["user_id"], "id": id}
	)
	media = result.fetchone()
	return media


def edit(fields: dict, shared: str, m_type: str, id: int):
	params = {**fields, "owner": session["user_id"], "shared": shared, "id": id}
	result = db.session.execute(SQL_EDIT[TYPES[TYPE_NAMES.index(m_type)]], params)
	media = result.fetchall()
	db.session.commit()
	return media[0]


def delete(m_type: str, id: int) -> None:
	params = {"owner": session["user_id"], "id": id}
	db.session.execute(SQL_DELETE[TYPES[TYPE_NAMES.index(m_type)]], params)
	db.session.commit()
