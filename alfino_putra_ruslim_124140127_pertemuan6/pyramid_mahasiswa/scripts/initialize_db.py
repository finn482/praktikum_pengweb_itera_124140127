"""Script seeding data awal aplikasi."""

import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models import Mahasiswa, Matakuliah


MATKUL_AWAL = [
    {"kode_mk": "IF2110", "nama_mk": "Pemrograman Web", "sks": 3, "semester": 5},
    {"kode_mk": "IF3140", "nama_mk": "Basis Data", "sks": 4, "semester": 3},
    {"kode_mk": "IF2120", "nama_mk": "Struktur Data", "sks": 3, "semester": 3},
]


def setup_models(dbsession):
    """Menambahkan data Mahasiswa dan Matakuliah awal."""
    _seed_mahasiswa(dbsession)
    _seed_matakuliah(dbsession)


def _seed_mahasiswa(dbsession):
    """Menambahkan data Mahasiswa jika NIM belum terdaftar."""
    mahasiswa_awal = [
        {
            "nim": "12345",
            "nama": "Budi Santoso",
            "jurusan": "Teknik Informatika",
            "tanggal_lahir": date(2000, 5, 15),
            "alamat": "Bandar Lampung",
        },
        {
            "nim": "54321",
            "nama": "Siti Aminah",
            "jurusan": "Teknik Informatika",
            "tanggal_lahir": date(2001, 8, 22),
            "alamat": "Lampung Selatan",
        },
    ]
    for data in mahasiswa_awal:
        exists = dbsession.query(Mahasiswa).filter_by(nim=data["nim"]).first()
        if exists is None:
            dbsession.add(Mahasiswa(**data))


def _seed_matakuliah(dbsession):
    """Menambahkan data Matakuliah jika kode MK belum terdaftar."""
    for data in MATKUL_AWAL:
        exists = dbsession.query(Matakuliah).filter_by(kode_mk=data["kode_mk"]).first()
        if exists is None:
            dbsession.add(Matakuliah(**data))


def parse_args(argv):
    """Membaca path konfigurasi Pyramid dari command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("config_uri", help="Contoh: development.ini")
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """Menjalankan seeding dalam transaction manager Pyramid."""
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)
    try:
        with env["request"].tm:
            setup_models(env["request"].dbsession)
        print("Seeding database selesai.")
    except OperationalError as error:
        print("Koneksi PostgreSQL gagal. Periksa DATABASE_URL.")
        print(error)
    finally:
        env["closer"]()


if __name__ == "__main__":
    main()
