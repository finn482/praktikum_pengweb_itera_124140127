# Praktikum Pemrograman Web — Pertemuan 6

## Identitas Praktikan

- **Nama:** Alfino Putra Ruslim
- **NIM:** 124140127
- **Program Studi:** Teknik Informatika
- **Kampus:** Institut Teknologi Sumatera (ITERA)
- **Kelas Praktikum:** RA

## Deskripsi Aplikasi

Aplikasi ini merupakan RESTful API sederhana berbasis Pyramid untuk mengelola data mahasiswa dan mata kuliah. Tugas pertemuan ini melanjutkan pola modul Mahasiswa dari praktikum sebelumnya dengan menambahkan modul Matakuliah, termasuk model SQLAlchemy, validasi input, route URL Dispatch, dan operasi CRUD.

Data disimpan di PostgreSQL. Alembic dipakai untuk mencatat perubahan struktur database, sedangkan data contoh dapat dimasukkan lewat script seeding. Script seeding mengecek NIM atau kode mata kuliah lebih dulu supaya tidak membuat data ganda saat dijalankan berulang.

## Teknologi

- Python 3
- Pyramid dan Waitress
- SQLAlchemy ORM
- PostgreSQL dengan driver `psycopg2`
- Alembic
- WebTest dan pytest untuk pengujian

## Struktur Direktori

```text
alfino_putra_ruslim_124140127_pertemuan6/
├── .gitignore
├── development.ini
├── production.ini
├── pytest.ini
├── setup.py
├── README.md
├── screenshots/
└── pyramid_mahasiswa/
    ├── __init__.py
    ├── routes.py
    ├── alembic/
    │   ├── env.py
    │   └── versions/
    ├── models/
    │   ├── __init__.py
    │   ├── meta.py
    │   ├── mahasiswa.py
    │   └── matakuliah.py
    ├── scripts/
    │   └── initialize_db.py
    ├── tests/
    │   ├── test_mahasiswa.py
    │   └── test_matakuliah.py
    └── views/
        ├── default.py
        ├── mahasiswa.py
        └── matakuliah.py
```

## Persyaratan

Pastikan komputer sudah memiliki:

- Python 3.10 atau lebih baru
- PostgreSQL dan `psql`
- Git (opsional, jika mengambil project dari GitHub)

Clone repository, lalu buka folder tugas ini di VS Code. Semua perintah berikut dijalankan dari terminal PowerShell pada folder `alfino_putra_ruslim_124140127_pertemuan6`.

## Instalasi dan Persiapan Database

### 1. Buat dan aktifkan virtual environment

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Kalau PowerShell menolak aktivasi script, jalankan perintah ini pada terminal yang sama, lalu aktifkan lagi:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 2. Instal project dan dependency

```powershell
python -m pip install --upgrade pip
pip install -e ".[testing]"
```

### 3. Buat database PostgreSQL

Pastikan service PostgreSQL sudah berjalan. Buat database (sesuaikan user PostgreSQL di komputer masing-masing):

```powershell
psql -U postgres -c "CREATE DATABASE pyramid_mahasiswa;"
```

Set connection string untuk sesi PowerShell saat ini. Ganti `PASSWORD` dengan password PostgreSQL lokal; jangan menyimpan password ini di file yang diunggah ke GitHub.

```powershell
$env:DATABASE_URL = "postgresql+psycopg2://postgres:PASSWORD@localhost:5432/pyramid_mahasiswa"
```

Jika user database yang digunakan tidak memiliki password, sesuaikan URL dengan aturan autentikasi PostgreSQL lokal. `development.ini` berisi URL contoh tanpa password; environment variable `DATABASE_URL` akan menggantikannya saat proses berjalan.

### 4. Jalankan migrasi

```powershell
alembic -c development.ini upgrade head
```

Migrasi awal membuat tabel `mahasiswa`, kemudian migrasi `55bd90e5cad8` membuat tabel `matakuliah`. Untuk membuat migrasi baru setelah mengubah model, jalankan autogenerate dan periksa file yang dihasilkan sebelum menerapkannya:

```powershell
alembic -c development.ini revision --autogenerate -m "deskripsi perubahan"
alembic -c development.ini upgrade head
```

### 5. Isi data awal

```powershell
python -m pyramid_mahasiswa.scripts.initialize_db development.ini
```

Script ini menambahkan contoh data Mahasiswa dan tiga mata kuliah berikut jika belum ada:

| Kode MK | Nama Mata Kuliah | SKS | Semester |
|---|---|---:|---:|
| IF2110 | Pemrograman Web | 3 | 5 |
| IF3140 | Basis Data | 4 | 3 |
| IF2120 | Struktur Data | 3 | 3 |

### 6. Jalankan server

```powershell
pserve development.ini
```

Server berjalan di `http://localhost:6543`. Hentikan dengan `Ctrl+C`.

## Dokumentasi Endpoint

Semua response menggunakan JSON. Endpoint tersedia untuk **Mahasiswa** (modul praktikum sebelumnya) dan **Matakuliah**.

### Mahasiswa

Field wajib saat menambah data: `nim`, `nama`, `jurusan`. `tanggal_lahir` menggunakan format `YYYY-MM-DD` dan `alamat` bersifat opsional.

| Method | URL | Fungsi |
|---|---|---|
| GET | `/api/mahasiswa` | Mengambil seluruh Mahasiswa |
| GET | `/api/mahasiswa/{id}` | Mengambil detail berdasarkan ID |
| POST | `/api/mahasiswa` | Menambahkan Mahasiswa; sukses `201`, data tidak valid atau NIM duplikat `400` |
| PUT | `/api/mahasiswa/{id}` | Memperbarui data; sukses `200`, ID tidak ditemukan `404` |
| DELETE | `/api/mahasiswa/{id}` | Menghapus data; sukses `200`, ID tidak ditemukan `404` |

Contoh request POST:

```json
{
  "nim": "124140127",
  "nama": "Alfino Putra Ruslim",
  "jurusan": "Teknik Informatika",
  "tanggal_lahir": "2004-01-01",
  "alamat": "Lampung Selatan"
}
```

Contoh response:

```json
{
  "success": true,
  "mahasiswa": {
    "id": 1,
    "nim": "124140127",
    "nama": "Alfino Putra Ruslim",
    "jurusan": "Teknik Informatika",
    "tanggal_lahir": "2004-01-01",
    "alamat": "Lampung Selatan"
  }
}
```

### Matakuliah

Field wajib: `kode_mk`, `nama_mk`, `sks`, dan `semester`. `sks` dan `semester` harus berupa integer positif. `kode_mk` harus unik.

| Method | URL | Fungsi |
|---|---|---|
| GET | `/api/matakuliah` | Mengambil seluruh mata kuliah; status `200` |
| GET | `/api/matakuliah/{id}` | Mengambil detail mata kuliah; `200` atau `404` |
| POST | `/api/matakuliah` | Menambahkan mata kuliah; `201`, input tidak valid/duplikat `400` |
| PUT | `/api/matakuliah/{id}` | Memperbarui data; `200`, input tidak valid `400`, ID tidak ditemukan `404` |
| DELETE | `/api/matakuliah/{id}` | Menghapus data; `200` atau `404` |

Contoh POST:

```json
{
  "kode_mk": "IF2150",
  "nama_mk": "Pemrograman Berorientasi Objek",
  "sks": 3,
  "semester": 5
}
```

Contoh response POST (`201 Created`):

```json
{
  "success": true,
  "matakuliah": {
    "id": 4,
    "kode_mk": "IF2150",
    "nama_mk": "Pemrograman Berorientasi Objek",
    "sks": 3,
    "semester": 5
  }
}
```

Response GET list berbentuk:

```json
{
  "matakuliah": [
    {
      "id": 1,
      "kode_mk": "IF2110",
      "nama_mk": "Pemrograman Web",
      "sks": 3,
      "semester": 5
    }
  ]
}
```

## Pengujian dengan cURL di PowerShell

Jalankan server di satu terminal PowerShell menggunakan `pserve development.ini`, lalu jalankan contoh berikut dari terminal PowerShell lain. Gunakan `curl.exe` agar perintah menjalankan cURL, bukan alias `Invoke-WebRequest` milik PowerShell. Pastikan setiap command berakhir dengan `-i` untuk melihat HTTP status.

### A. GET seluruh Matakuliah

```powershell
curl.exe -i http://localhost:6543/api/matakuliah
```

Tujuan: mengambil daftar mata kuliah. Diharapkan **HTTP 200**.

Contoh response:

```json
{"matakuliah":[{"id":1,"kode_mk":"IF2110","nama_mk":"Pemrograman Web","sks":3,"semester":5}]}
```

### B. GET detail Matakuliah

```powershell
curl.exe -i http://localhost:6543/api/matakuliah/1
```

Tujuan: melihat mata kuliah dengan ID 1. Diharapkan **HTTP 200** jika ada.

```json
{"matakuliah":{"id":1,"kode_mk":"IF2110","nama_mk":"Pemrograman Web","sks":3,"semester":5}}
```

### C. POST tambah Matakuliah

```powershell
curl.exe -i -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" -d '{"kode_mk":"IF2150","nama_mk":"Pemrograman Berorientasi Objek","sks":3,"semester":5}'
```

Tujuan: menambahkan data baru. Diharapkan **HTTP 201**; ID di response dibuat oleh database.

```json
{"success":true,"matakuliah":{"id":4,"kode_mk":"IF2150","nama_mk":"Pemrograman Berorientasi Objek","sks":3,"semester":5}}
```

### D. PUT ubah Matakuliah

Jalankan setelah POST dan ganti `4` dengan ID yang didapat dari response POST.

```powershell
curl.exe -i -X PUT http://localhost:6543/api/matakuliah/4 -H "Content-Type: application/json" -d '{"kode_mk":"IF2150","nama_mk":"Pemrograman Berorientasi Objek Lanjut","sks":4,"semester":6}'
```

Tujuan: memperbarui data. Diharapkan **HTTP 200**.

```json
{"success":true,"matakuliah":{"id":4,"kode_mk":"IF2150","nama_mk":"Pemrograman Berorientasi Objek Lanjut","sks":4,"semester":6}}
```

### E. DELETE Matakuliah

```powershell
curl.exe -i -X DELETE http://localhost:6543/api/matakuliah/4
```

Tujuan: menghapus data dengan ID tersebut. Diharapkan **HTTP 200**.

```json
{"success":true,"message":"Matakuliah berhasil dihapus"}
```

### Uji validasi dan error

Skenario berikut diharapkan menghasilkan response error JSON dengan status yang dicantumkan. Contoh pesannya mengikuti implementasi saat ini.

| Tujuan | Perintah PowerShell | Status yang diharapkan | Contoh response |
|---|---|---:|---|
| ID tidak ditemukan | `curl.exe -i http://localhost:6543/api/matakuliah/999` | 404 | `{"error":"Matakuliah tidak ditemukan"}` |
| Field wajib tidak lengkap | `curl.exe -i -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" -d '{"kode_mk":"IF2200","nama_mk":"Jaringan Komputer","sks":3}'` | 400 | `{"error":"Field semester wajib diisi"}` |
| Kode MK duplikat (gunakan kode yang sudah ada) | `curl.exe -i -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" -d '{"kode_mk":"IF2110","nama_mk":"Duplikat","sks":3,"semester":5}'` | 400 | `{"error":"Kode mata kuliah sudah digunakan"}` |
| SKS negatif | `curl.exe -i -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" -d '{"kode_mk":"IF2201","nama_mk":"Jaringan Komputer","sks":-1,"semester":3}'` | 400 | `{"error":"Field sks harus berupa integer positif"}` |
| Semester nol | `curl.exe -i -X POST http://localhost:6543/api/matakuliah -H "Content-Type: application/json" -d '{"kode_mk":"IF2202","nama_mk":"Jaringan Komputer","sks":3,"semester":0}'` | 400 | `{"error":"Field semester harus berupa integer positif"}` |
| PUT SKS tidak valid | `curl.exe -i -X PUT http://localhost:6543/api/matakuliah/1 -H "Content-Type: application/json" -d '{"sks":-2}'` | 400 | `{"error":"Field sks harus berupa integer positif"}` |
| DELETE ID tidak ditemukan | `curl.exe -i -X DELETE http://localhost:6543/api/matakuliah/999` | 404 | `{"error":"Matakuliah tidak ditemukan"}` |

Skenario tambahan: untuk mencoba DELETE atau PUT yang sukses, tambahkan data dulu dengan POST dan gunakan ID yang dikembalikan. Request dengan kode mata kuliah berulang menolak duplikasi sebelum data disimpan.

## Pengujian Otomatis

Setelah PostgreSQL berjalan, migrasi diterapkan, dan `DATABASE_URL` disetel pada PowerShell yang sama:

```powershell
python -m pytest -q
```

Pengujian mencakup validasi dan operasi Matakuliah serta beberapa endpoint Mahasiswa untuk memastikan modul sebelumnya tetap berfungsi. Saat menulis README ini, rangkaian pengujian dijalankan pada PostgreSQL lokal: **16 passed**. Pyramid juga menampilkan warning deprecation `pkg_resources` dari dependency; warning tersebut tidak menghentikan test.

## Bukti Screenshot Pengujian

Screenshot belum disertakan agar tidak menampilkan gambar bukti yang tidak benar-benar diambil. Jalankan aplikasi dan pengujian di terminal, lalu simpan screenshot asli di folder `screenshots/` dengan nama berikut:

1. `screenshots/01-get-matakuliah.png` — hasil GET seluruh mata kuliah beserta status `200`.
2. `screenshots/02-post-matakuliah.png` — hasil POST data baru beserta status `201`.
3. `screenshots/03-put-delete-matakuliah.png` — hasil PUT dan DELETE beserta statusnya.
4. `screenshots/04-validasi-matakuliah.png` — contoh error validasi (misalnya SKS negatif) dengan status `400`.
5. `screenshots/05-pytest.png` — hasil `python -m pytest -q`.
6. `screenshots/06-mahasiswa-api.png` — contoh request/response endpoint Mahasiswa.

Setelah screenshot dibuat, sematkan dengan Markdown, misalnya:

```markdown
![Hasil GET seluruh Matakuliah](screenshots/01-get-matakuliah.png)
```

## Catatan Implementasi

- `Matakuliah` memakai `Base` yang sama dengan model Mahasiswa. `to_dict()` mengembalikan semua kolom untuk response JSON.
- Validator model dan controller memastikan `sks` serta `semester` merupakan integer positif; boolean juga ditolak walaupun di Python `bool` merupakan turunan `int`.
- Route menggunakan URL Dispatch Pyramid dengan predikat method HTTP, sehingga endpoint list dan detail tidak tertukar.
- Controller memakai `request.dbsession`, mengecek kode mata kuliah duplikat, dan melakukan rollback ketika terjadi error database.
- Alembic membaca metadata dari `pyramid_mahasiswa.models`; file migrasi dibuat dengan `--autogenerate`, bukan ditulis manual.
- `.gitignore` mengecualikan virtual environment, cache, database lokal, dan konfigurasi environment berisi kredensial.
