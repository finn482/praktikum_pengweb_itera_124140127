"""View controller CRUD Matakuliah."""

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..models import Matakuliah

REQUIRED_FIELDS = ("kode_mk", "nama_mk", "sks", "semester")
TEXT_FIELDS = ("kode_mk", "nama_mk")
NUMBER_FIELDS = ("sks", "semester")


def _validate_payload(data, require_all=False):
    """Memvalidasi payload dan mengembalikan data yang sudah dibersihkan."""
    if not isinstance(data, dict):
        raise ValueError("Payload harus berupa objek JSON")

    if require_all:
        missing = next(
            (field for field in REQUIRED_FIELDS if field not in data),
            None,
        )
        if missing:
            raise ValueError(f"Field {missing} wajib diisi")

    cleaned = {}
    for field in TEXT_FIELDS:
        if field in data:
            value = data[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Field {field} wajib berupa teks dan tidak boleh kosong")
            cleaned[field] = value.strip()

    for field in NUMBER_FIELDS:
        if field in data:
            value = data[field]
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"Field {field} harus berupa integer positif")
            cleaned[field] = value

    if not cleaned:
        raise ValueError("Tidak ada data yang dapat diperbarui")

    return cleaned


def _duplicate_code(dbsession, kode_mk, current_id=None):
    """Memeriksa apakah kode mata kuliah sudah digunakan item lain."""
    query = dbsession.query(Matakuliah).filter(Matakuliah.kode_mk == kode_mk)
    if current_id is not None:
        query = query.filter(Matakuliah.id != current_id)
    return query.first() is not None


def _bad_request(message):
    """Membuat response HTTP 400 yang konsisten."""
    return HTTPBadRequest(json_body={"error": message})


@view_config(route_name="matakuliah_list", renderer="json")
def matakuliah_list(request):
    """Mengambil seluruh mata kuliah."""
    rows = request.dbsession.query(Matakuliah).order_by(Matakuliah.id).all()
    return {"matakuliah": [row.to_dict() for row in rows]}


@view_config(route_name="matakuliah_detail", renderer="json")
def matakuliah_detail(request):
    """Mengambil satu mata kuliah berdasarkan ID."""
    matakuliah = request.dbsession.get(Matakuliah, request.matchdict["id"])
    if matakuliah is None:
        return HTTPNotFound(json_body={"error": "Matakuliah tidak ditemukan"})
    return {"matakuliah": matakuliah.to_dict()}


@view_config(route_name="matakuliah_add", renderer="json")
def matakuliah_add(request):
    """Menambahkan mata kuliah dari payload JSON."""
    try:
        data = _validate_payload(request.json_body, require_all=True)
        if _duplicate_code(request.dbsession, data["kode_mk"]):
            return _bad_request("Kode mata kuliah sudah digunakan")

        matakuliah = Matakuliah(**data)
        request.dbsession.add(matakuliah)
        request.dbsession.flush()
        request.response.status_code = 201
        return {"success": True, "matakuliah": matakuliah.to_dict()}
    except (TypeError, ValueError) as error:
        return _bad_request(str(error) or "Format data tidak valid")
    except IntegrityError:
        request.dbsession.rollback()
        return _bad_request("Kode mata kuliah sudah digunakan")
    except SQLAlchemyError:
        request.dbsession.rollback()
        return _bad_request("Operasi database gagal")


@view_config(route_name="matakuliah_update", renderer="json")
def matakuliah_update(request):
    """Memperbarui mata kuliah berdasarkan ID."""
    matakuliah = request.dbsession.get(Matakuliah, request.matchdict["id"])
    if matakuliah is None:
        return HTTPNotFound(json_body={"error": "Matakuliah tidak ditemukan"})

    try:
        data = _validate_payload(request.json_body)
        kode_mk = data.get("kode_mk")
        if kode_mk and _duplicate_code(
            request.dbsession,
            kode_mk,
            current_id=matakuliah.id,
        ):
            return _bad_request("Kode mata kuliah sudah digunakan")

        for field, value in data.items():
            setattr(matakuliah, field, value)
        request.dbsession.flush()
        return {"success": True, "matakuliah": matakuliah.to_dict()}
    except (TypeError, ValueError) as error:
        return _bad_request(str(error) or "Format data tidak valid")
    except IntegrityError:
        request.dbsession.rollback()
        return _bad_request("Kode mata kuliah sudah digunakan")
    except SQLAlchemyError:
        request.dbsession.rollback()
        return _bad_request("Operasi database gagal")


@view_config(route_name="matakuliah_delete", renderer="json")
def matakuliah_delete(request):
    """Menghapus mata kuliah berdasarkan ID."""
    matakuliah = request.dbsession.get(Matakuliah, request.matchdict["id"])
    if matakuliah is None:
        return HTTPNotFound(json_body={"error": "Matakuliah tidak ditemukan"})

    try:
        request.dbsession.delete(matakuliah)
        request.dbsession.flush()
        return {"success": True, "message": "Matakuliah berhasil dihapus"}
    except SQLAlchemyError:
        request.dbsession.rollback()
        return _bad_request("Operasi database gagal")
