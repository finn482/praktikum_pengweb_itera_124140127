"""View controller CRUD Mahasiswa."""

from datetime import date

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..models import Mahasiswa

REQUIRED_FIELDS = ("nim", "nama", "jurusan")


def _parse_date(value):
    """Mengubah string YYYY-MM-DD menjadi date atau None."""
    if not value:
        return None
    return date.fromisoformat(value)


def _required_error(data):
    """Mengembalikan nama field wajib yang kosong."""
    return next((field for field in REQUIRED_FIELDS if not data.get(field)), None)


@view_config(route_name="mahasiswa_list", renderer="json")
def mahasiswa_list(request):
    """Mengambil seluruh mahasiswa."""
    rows = request.dbsession.query(Mahasiswa).order_by(Mahasiswa.id).all()
    return {"mahasiswas": [row.to_dict() for row in rows]}


@view_config(route_name="mahasiswa_detail", renderer="json")
def mahasiswa_detail(request):
    """Mengambil satu mahasiswa berdasarkan ID."""
    mahasiswa = request.dbsession.get(Mahasiswa, request.matchdict["id"])
    if mahasiswa is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan"})
    return {"mahasiswa": mahasiswa.to_dict()}


@view_config(route_name="mahasiswa_add", renderer="json")
def mahasiswa_add(request):
    """Menambahkan mahasiswa dari payload JSON."""
    try:
        data = request.json_body
        missing = _required_error(data)
        if missing:
            return HTTPBadRequest(json_body={"error": f"Field {missing} wajib diisi"})
        mahasiswa = Mahasiswa(
            nim=data["nim"],
            nama=data["nama"],
            jurusan=data["jurusan"],
            tanggal_lahir=_parse_date(data.get("tanggal_lahir")),
            alamat=data.get("alamat"),
        )
        request.dbsession.add(mahasiswa)
        request.dbsession.flush()
        request.response.status_code = 201
        return {"success": True, "mahasiswa": mahasiswa.to_dict()}
    except (TypeError, ValueError):
        return HTTPBadRequest(json_body={"error": "Format data tidak valid"})
    except IntegrityError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={"error": "NIM sudah digunakan"})
    except SQLAlchemyError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={"error": "Operasi database gagal"})


@view_config(route_name="mahasiswa_update", renderer="json")
def mahasiswa_update(request):
    """Memperbarui mahasiswa berdasarkan ID."""
    mahasiswa = request.dbsession.get(Mahasiswa, request.matchdict["id"])
    if mahasiswa is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan"})
    try:
        data = request.json_body
        for field in ("nim", "nama", "jurusan", "alamat"):
            if field in data:
                setattr(mahasiswa, field, data[field])
        if "tanggal_lahir" in data:
            mahasiswa.tanggal_lahir = _parse_date(data["tanggal_lahir"])
        request.dbsession.flush()
        return {"success": True, "mahasiswa": mahasiswa.to_dict()}
    except (TypeError, ValueError):
        return HTTPBadRequest(json_body={"error": "Format data tidak valid"})
    except IntegrityError:
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={"error": "NIM sudah digunakan"})


@view_config(route_name="mahasiswa_delete", renderer="json")
def mahasiswa_delete(request):
    """Menghapus mahasiswa berdasarkan ID."""
    mahasiswa = request.dbsession.get(Mahasiswa, request.matchdict["id"])
    if mahasiswa is None:
        return HTTPNotFound(json_body={"error": "Mahasiswa tidak ditemukan"})
    request.dbsession.delete(mahasiswa)
    return {"success": True, "message": "Mahasiswa berhasil dihapus"}
