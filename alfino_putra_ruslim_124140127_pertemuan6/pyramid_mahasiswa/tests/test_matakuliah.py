"""Uji CRUD dan validasi Matakuliah menggunakan WebTest terhadap PostgreSQL."""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from webtest import TestApp

from pyramid_mahasiswa import main
from pyramid_mahasiswa.models import Base

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
    """Mengosongkan tabel matakuliah sebelum setiap test."""
    session = sessionmaker(bind=engine)()
    try:
        session.execute(text("TRUNCATE matakuliah RESTART IDENTITY CASCADE"))
        session.commit()
    finally:
        session.close()
    yield


def _post(app, payload, expect_status=201):
    """Membantu memanggil POST dengan payload dan status yang diharapkan."""
    resp = app.post_json("/api/matakuliah", params=payload, status=expect_status)
    return resp


def test_get_empty_list(app, clean_db):
    """GET /api/matakuliah mengembalikan daftar kosong."""
    resp = app.get("/api/matakuliah")
    assert resp.status_code == 200
    assert resp.json["matakuliah"] == []


def test_create_matakuliah(app, clean_db):
    """POST valid mengembalikan 201 dan menampilkan data yang dibuat."""
    payload = {
        "kode_mk": "IF2150",
        "nama_mk": "Pemrograman Berorientasi Objek",
        "sks": 3,
        "semester": 5,
    }
    resp = _post(app, payload)
    assert resp.status_code == 201
    body = resp.json["matakuliah"]
    assert body["kode_mk"] == "IF2150"
    assert body["nama_mk"] == "Pemrograman Berorientasi Objek"
    assert body["sks"] == 3
    assert body["semester"] == 5
    assert body["id"] == 1


def test_create_missing_field(app, clean_db):
    """POST tanpa field wajib mengembalikan 400 dengan pesan error."""
    resp = _post(app, {"kode_mk": "IF2200", "nama_mk": "Jaringan Komputer"}, expect_status=400)
    assert "wajib diisi" in resp.json["error"]


def test_create_duplicate_code(app, clean_db):
    """POST kode_mk duplikat mengembalikan 400."""
    _post(app, {"kode_mk": "IF2110", "nama_mk": "Pemrograman Web", "sks": 3, "semester": 5})
    resp = _post(
        app,
        {"kode_mk": "IF2110", "nama_mk": "Pemrograman Web Lanjut", "sks": 2, "semester": 6},
        expect_status=400,
    )
    assert "sudah digunakan" in resp.json["error"]


def test_create_negative_sks(app, clean_db):
    """POST SKS negatif mengembalikan 400."""
    resp = _post(
        app,
        {"kode_mk": "IF2160", "nama_mk": "Sistem Operasi", "sks": -1, "semester": 3},
        expect_status=400,
    )
    assert "integer positif" in resp.json["error"]


def test_create_zero_semester(app, clean_db):
    """POST semester nol mengembalikan 400."""
    resp = _post(
        app,
        {"kode_mk": "IF2170", "nama_mk": "Metode Numerik", "sks": 3, "semester": 0},
        expect_status=400,
    )
    assert "integer positif" in resp.json["error"]


def test_get_detail(app, clean_db):
    """GET detail mengembalikan 200 dengan data yang diminta."""
    created = _post(
        app,
        {"kode_mk": "IF3140", "nama_mk": "Basis Data", "sks": 4, "semester": 3},
    ).json["matakuliah"]
    resp = app.get(f"/api/matakuliah/{created['id']}")
    assert resp.status_code == 200
    assert resp.json["matakuliah"]["kode_mk"] == "IF3140"


def test_get_detail_not_found(app, clean_db):
    """GET detail ID yang tidak ada mengembalikan 404."""
    resp = app.get("/api/matakuliah/999", status=404)
    assert "tidak ditemukan" in resp.json["error"]


def test_update_matakuliah(app, clean_db):
    """PUT valid mengembalikan 200 dan data berubah."""
    created = _post(
        app,
        {"kode_mk": "IF2150", "nama_mk": "Pemrograman Berorientasi Objek", "sks": 3, "semester": 5},
    ).json["matakuliah"]
    resp = app.put_json(
        f"/api/matakuliah/{created['id']}",
        params={"nama_mk": "Pemrograman Berorientasi Objek Lanjut", "sks": 4, "semester": 6},
    )
    assert resp.status_code == 200
    body = resp.json["matakuliah"]
    assert body["nama_mk"] == "Pemrograman Berorientasi Objek Lanjut"
    assert body["sks"] == 4
    assert body["semester"] == 6


def test_update_not_found(app, clean_db):
    """PUT ID yang tidak ada mengembalikan 404."""
    resp = app.put_json(
        "/api/matakuliah/999",
        params={"nama_mk": "Basis Data Lanjut"},
        status=404,
    )
    assert "tidak ditemukan" in resp.json["error"]


def test_update_invalid_sks(app, clean_db):
    """PUT dengan data tidak valid mengembalikan 400."""
    created = _post(
        app,
        {"kode_mk": "IF2150", "nama_mk": "Pemrograman Berorientasi Objek", "sks": 3, "semester": 5},
    ).json["matakuliah"]
    resp = app.put_json(f"/api/matakuliah/{created['id']}", params={"sks": -2}, status=400)
    assert "integer positif" in resp.json["error"]


def test_delete_matakuliah(app, clean_db):
    """DELETE valid mengembalikan 200."""
    created = _post(
        app,
        {"kode_mk": "IF2120", "nama_mk": "Struktur Data", "sks": 3, "semester": 3},
    ).json["matakuliah"]
    resp = app.delete(f"/api/matakuliah/{created['id']}")
    assert resp.status_code == 200
    assert resp.json["success"] is True


def test_delete_not_found(app, clean_db):
    """DELETE ID yang tidak ada mengembalikan 404."""
    resp = app.delete("/api/matakuliah/999", status=404)
    assert "tidak ditemukan" in resp.json["error"]
