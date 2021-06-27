import re

from db import db
from flask import session

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
	"film": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Length(min)", "type": "number", "min": 0, "max": 2000, "required": False},
		{"name": "Director", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Writer", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Star", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Watched(owner)", "type": "checkbox", "required": True},
		{"name": "Shared", "type": "checkbox", "required": True}
	],
	"music": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Inteprator", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Composer", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Lyricist", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Shared", "type": "checkbox", "required": True}
	],
	"book": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Pages", "type": "text", "min": 0, "max": 100000, "required": False},
		{"name": "Author", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Read(owner)", "type": "checkbox", "required": True},
		{"name": "Shared", "type": "checkbox", "required": True}
	],
	"comic": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Pages", "type": "text", "min": 0, "max": 100000, "required": False},
		{"name": "Author", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Illustrator", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Read(owner)", "type": "checkbox", "required": True},
		{"name": "Shared", "type": "checkbox", "required": True}
	],
	"game": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Developer", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Platform", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Publisher", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Completed(owner)", "type": "checkbox", "required": True},
		{"name": "Shared", "type": "checkbox", "required": True}
	],
	"other": [
		{"name": "Title", "type": "text", "min": 1, "max": 255, "required": True},
		{"name": "Published", "type": "number", "min": 0, "max": 3000, "required": False},
		{"name": "Genres", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Information", "type": "text", "min": 0, "max": 255, "required": False},
		{"name": "Shared", "type": "checkbox", "required": True}
	]
}

SQL_BROWSE = {
	"film": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m."Length(min)" AS "Length(min)", m.Director AS Director,
			m.Writer AS Writer, m.Star AS Star, m."Watched(owner)" AS "Watched(owner)",
			m.Shared AS Shared
		FROM films AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
	"music": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Inteprator AS Inteprator, m.Composer AS Composer,
			m.Lyricist AS Lyricist, m.Shared AS Shared
		FROM music AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
	"book": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Pages AS Pages, m.Author AS Author,
			m."Read(owner)" AS "Read(owner)", m.Shared AS Shared
		FROM books AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
	"comic": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Pages AS Pages, m.Author AS Author, m.Illustrator AS Illustrator,
			m."Read(owner)" AS "Read(owner)", m.Shared AS Shared
		FROM comics AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
	"game": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Developer AS Developer, m.Platform AS Platform,
			m.Publisher AS Publisher, m."Completed(owner)" AS "Completed(owner)", m.Shared AS Shared
		FROM games AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
	"other": """
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Information AS Information, m.Shared AS Shared
		FROM other AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner=:owner AND m.Title ~* :pattern
	""",
}

SQL_BROWSE_FRIENDS = {
	"film": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m."Length(min)" AS "Length(min)", m.Director AS Director,
			m.Writer AS Writer, m.Star AS Star, m."Watched(owner)" AS "Watched(owner)",
			m.Shared AS Shared
		FROM films AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
	"music": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Inteprator AS Inteprator, m.Composer AS Composer,
			m.Lyricist AS Lyricist, m.Shared AS Shared
		FROM music AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
	"book": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Pages AS Pages, m.Author AS Author,
			m."Read(owner)" AS "Read(owner)", m.Shared AS Shared
		FROM books AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
	"comic": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Pages AS Pages, m.Author AS Author, m.Illustrator AS Illustrator,
			m."Read(owner)" AS "Read(owner)", m.Shared AS Shared
		FROM comics AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
	"game": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Developer AS Developer, m.Platform AS Platform,
			m.Publisher AS Publisher, m."Completed(owner)" AS "Completed(owner)", m.Shared AS Shared
		FROM games AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
	"other": """
		WITH friends AS (
			SELECT friend AS id
			FROM friends
			WHERE "user"=:owner
		)
		SELECT m.id AS id, u.username AS owner, m.Title AS Title, m.Published AS Published,
			m.Genres AS Genres, m.Information AS Information, m.Shared AS Shared
		FROM other AS m
		JOIN users AS u ON u.id=m.owner
		WHERE m.owner IN (SELECT id FROM friends) AND m.Title ~* :pattern AND m.shared
	""",
}

SQL_INSERT = {
	"film": """
		INSERT INTO films (owner, Title, Published, Genres, "Length(min)", Director, Writer, Star,
			"Watched(owner)", Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Lengthmin, :Director, :Writer, :Star,
			:Watchedowner, :Shared)
	""",
	"music": """
		INSERT INTO music (owner, Title, Published, Genres, Inteprator, Composer, Lyricist, Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Inteprator, :Composer, :Lyricist, :Shared)
	""",
	"book": """
		INSERT INTO books (owner, Title, Published, Genres, Pages, Author, "Read(owner)", Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Pages, :Author, :Readowner, :Shared)
	""",
	"comic": """
		INSERT INTO comics (owner, Title, Published, Genres, Pages, Author, "Read(owner)", Illustrator,
			Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Pages, :Author, :Readowner, :Illustrator,
			:Shared)
	""",
	"game": """
		INSERT INTO games (owner, Title, Published, Genres, Developer, Platform, Publisher,
			"Completed(owner)", Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Developer, :Platform, :Publisher,
			:Completedowner, :Shared)
	""",
	"other": """
		INSERT INTO other (owner, Title, Published, Genres, Information, Shared)
		VALUES (:owner, :Title, :Published, :Genres, :Information, :Shared)
	"""
}

SQL_GET = {
	"film": "SELECT * FROM films WHERE owner=:owner AND id=:id",
	"music": "SELECT * FROM music WHERE owner=:owner AND id=:id",
	"book": "SELECT * FROM books WHERE owner=:owner AND id=:id",
	"comic": "SELECT * FROM comics WHERE owner=:owner AND id=:id",
	"game": "SELECT * FROM games WHERE owner=:owner AND id=:id",
	"other": "SELECT * FROM other WHERE owner=:owner AND id=:id",
}

SQL_EDIT = {
	"film": """
		UPDATE films
		SET Title=:Title, Published=:Published, Genres=:Genres, "Length(min)"=:Lengthmin,
			Director=:Director, Writer=:Writer, Star=:Star, "Watched(owner)"=:Watchedowner,
			Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	""",
	"music": """
		UPDATE music
		SET Title=:Title, Published=:Published, Genres=:Genres, Inteprator=:Inteprator,
			Composer=:Composer, Lyricist=:Lyricist, Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	""",
	"book": """
		UPDATE books
		SET Title=:Title, Published=:Published, Genres=:Genres, Pages=:Pages, Author=:Author,
			"Read(owner)"=:Readowner, Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	""",
	"comic": """
		UPDATE comics
		SET Title=:Title, Published=:Published, Genres=:Genres, Pages=:Pages, Author=:Author,
			Illustrator=:Illustrator, "Read(owner)"=:Readowner, Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	""",
	"game": """
		UPDATE games
		SET Title=:Title, Published=:Published, Genres=:Genres, Developer=:Developer,
			Platform=:Platform, Publisher=:Publisher, "Completed(owner)"=:Completedowner,
			Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	""",
	"other": """
		UPDATE other
		SET Title=:Title, Published=:Published, Genres=:Genres, Information=:Information,
			Shared=:Shared
		WHERE owner=:owner AND id=:id RETURNING *
	"""
}

SQL_DELETE = {
	"film": "DELETE FROM films WHERE owner=:owner AND id=:id",
	"music": "DELETE FROM music WHERE owner=:owner AND id=:id",
	"book": "DELETE FROM books WHERE owner=:owner AND id=:id",
	"comic": "DELETE FROM comics WHERE owner=:owner AND id=:id",
	"game": "DELETE FROM games WHERE owner=:owner AND id=:id",
	"other": "DELETE FROM other WHERE owner=:owner AND id=:id",
}


def fix_params(params: dict):
	"""I can't use SQLAlchemy, this removes brackets and changes empty string to None"""
	def empty_to_null(v):
		if v == "":
			return None
		return v
	return {re.sub(r"[\(\)]", "", k): empty_to_null(v) for k, v in params.items()}


def browse(pattern: str, m_type: str):
	result = db.session.execute(
		SQL_BROWSE[m_type],
		{"pattern": re.escape(pattern), "owner": session["user_id"]}
	)
	rows = result.fetchall()
	return rows


def browse_friends(pattern: str, m_type: str):
	result = db.session.execute(
		SQL_BROWSE_FRIENDS[m_type],
		{"pattern": re.escape(pattern), "owner": session["user_id"]}
	)
	rows = result.fetchall()
	return rows


def create(fields: dict, type: str) -> None:
	params = {**fields, "owner": session["user_id"]}
	db.session.execute(SQL_INSERT[type], fix_params(params))
	db.session.commit()


def get(m_type: str, id: int):
	result = db.session.execute(SQL_GET[m_type], {"owner": session["user_id"], "id": id})
	media = result.fetchone()
	return media


def edit(fields: dict, m_type: str, id: int):
	params = {**fields, "owner": session["user_id"], "id": id}
	result = db.session.execute(SQL_EDIT[m_type], fix_params(params))
	media = result.fetchone()
	db.session.commit()
	return media


def delete(m_type: str, id: int) -> None:
	params = {"owner": session["user_id"], "id": id}
	db.session.execute(SQL_DELETE[m_type], params)
	db.session.commit()


def fill_values_from_dict(values: dict, m_type: str) -> dict:
	fields = FIELDS[m_type].copy()
	for field in fields:
		field["value"] = values[field["name"]]
	return fields


def fill_values_from_row(row, m_type: str) -> dict:
	fields = FIELDS[m_type].copy()
	row = dict(row)
	for field in fields:
		if not field["name"] in row:
			field["value"] = row[field["name"].lower()]
		else:
			field["value"] = row[field["name"]]
	return fields
