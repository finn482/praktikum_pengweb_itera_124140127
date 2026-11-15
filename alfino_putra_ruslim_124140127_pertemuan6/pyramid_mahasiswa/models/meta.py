"""Declarative Base yang dipakai seluruh model SQLAlchemy."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base tunggal untuk metadata model aplikasi."""
