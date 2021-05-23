from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv

def createTables(db: SQLAlchemy):
	db.session.execute("""
		CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			username VARCHAR(20) NOT NULL UNIQUE,
			email VARCHAR(255) NOT NULL UNIQUE,
			password_hash TEXT NOT NULL
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS friends (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			user1 BIGINT,
			user2 BIGINT,
			FOREIGN KEY(user1) REFERENCES users(id) ON DELETE CASCADE,
			FOREIGN KEY(user2) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS friendrequests (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			user1 BIGINT,
			user2 BIGINT,
			FOREIGN KEY(user1) REFERENCES users(id) ON DELETE CASCADE,
			FOREIGN KEY(user2) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS films (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS music (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS books (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS comics (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS games (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")

	db.session.execute("""
		CREATE TABLE IF NOT EXISTS other (
			id SERIAL PRIMARY KEY NOT NULL UNIQUE,
			owner BIGINT,
			name TEXT NOT NULL,
			shared BOOLEAN DEFAULT '0',
			FOREIGN KEY(owner) REFERENCES users(id) ON DELETE CASCADE
		)
	""")
