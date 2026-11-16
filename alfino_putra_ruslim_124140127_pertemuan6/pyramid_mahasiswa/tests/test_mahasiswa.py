"""Uji endpoint Mahasiswa agar modul lama tetap berfungsi."""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from webtest import TestApp

from pyramid_mahasiswa import main

DATABASE_URL = "postgresql+psycopg2://postgres@localhost:55432/pyramid_mahasiswa"


@pytest.fixture(scope="session")
def engine():
    """Membuat engine bersama untuk seluruh test."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)


@pytest.fixture(scope="session")
def app(engine):
    """Membuat aplikasi WSGI yang memakai database test."""
    settings = {
        "sqlalchemy.url": DATABASE_URL,
        "tm.manager_hook": "pyramid_tm.explicit_manager",
    }
    return TestApp(main({}, **settings))


@pytest.fixture()
def clean_db(engine):
    """Mengosongkan tabel mahasiswa sebelum setiap test."""
    session = sessionmaker(bind=engine)()
    try:
        session.execute(text("TRUNCATE mahasiswa RESTART IDENTITY CASCADE"))
        session.commit()
    finally:
        session.close()
    yield


def test_mahasiswa_list_empty(app, clean_db):
    """GET /api/mahasiswa mengembalikan 200 dan daftar kosong."""
    resp = app.get("/api/mahasiswa")
    assert resp.status_code == 200
    assert resp.json["mahasiswas"] == []


def test_mahasiswa_create_and_get(app, clean_db):
    """POST lalu GET detail mahasiswa berjalan normal."""
    payload = {
        "nim": "124140127",
        "nama": "Alfino Putra Ruslim",
        "jurusan": "Teknik Informatika",
    }
    created = app.post_json("/api/mahasiswa", params=payload, status=201).json["mahasiswa"]
    assert created["nim"] == "124140127"

    detail = app.get(f"/api/mahasiswa/{created['id']}")
    assert detail.status_code == 200
    assert detail.json["mahasiswa"]["nama"] == "Alfino Putra Ruslim"


def test_mahasiswa_duplicate_nim(app, clean_db):
    """POST NIM duplikat mengembalikan 400."""
    payload = {
        "nim": "12345",
        "nama": "Budi Santoso",
        "jurusan": "Teknik Informatika",
    }
    app.post_json("/api/mahasiswa", params=payload, status=201)
    resp = app.post_json("/api/mahasiswa", params=payload, status=400)
    assert "sudah digunakan" in resp.json["error"]
