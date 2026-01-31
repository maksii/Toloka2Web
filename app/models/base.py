"""Base module for SQLAlchemy database instance."""

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
