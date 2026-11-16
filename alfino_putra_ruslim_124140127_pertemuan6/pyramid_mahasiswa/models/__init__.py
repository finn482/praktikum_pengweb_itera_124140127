"""Konfigurasi engine, session, dan registrasi model SQLAlchemy."""

import os

import zope.sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy.orm import configure_mappers, sessionmaker

from .mahasiswa import Mahasiswa
from .matakuliah import Matakuliah
from .meta import Base

configure_mappers()


def get_engine(settings, prefix="sqlalchemy."):
    """Membuat engine berdasarkan konfigurasi Pyramid atau DATABASE_URL."""
    settings = dict(settings)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        settings[f"{prefix}url"] = database_url
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    """Membuat factory session yang terhubung ke engine."""
    return sessionmaker(bind=engine)


def get_tm_session(session_factory, transaction_manager):
    """Membuat session yang mengikuti transaction manager Pyramid."""
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """Mendaftarkan request.dbsession ke aplikasi Pyramid."""
    settings = config.get_settings()
    settings["tm.manager_hook"] = "pyramid_tm.explicit_manager"
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry["dbsession_factory"] = session_factory
    config.registry["dbengine"] = engine
    config.add_request_method(
        lambda request: get_tm_session(session_factory, request.tm),
        "dbsession",
        reify=True,
    )


__all__ = ["Base", "Mahasiswa", "Matakuliah"]
