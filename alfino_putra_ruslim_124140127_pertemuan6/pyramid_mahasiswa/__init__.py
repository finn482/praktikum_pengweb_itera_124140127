"""Konfigurasi utama aplikasi Pyramid."""

import os

from pyramid.config import Configurator


def main(global_config, **settings):
    """Membuat dan mengembalikan aplikasi WSGI Pyramid."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        settings["sqlalchemy.url"] = database_url

    with Configurator(settings=settings) as config:
        config.include("pyramid_tm")
        config.include(".models")
        config.include(".routes")
        config.scan(".views")
        return config.make_wsgi_app()
