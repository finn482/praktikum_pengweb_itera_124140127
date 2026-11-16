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

## Pengujian API di PowerShell

Jalankan server di satu terminal PowerShell dengan `pserve development.ini`, lalu jalankan pengujian dari terminal kedua. Di Windows, pengiriman JSON lewat `curl.exe -d` kadang terkendala quoting. Contoh di bawah memakai library `requests`, yang mengirim JSON dengan benar.

Kalau `requests` belum terpasang, jalankan sekali:

```powershell
pip install requests
```

Contoh perintah Python berikut bisa dimasukkan di PowerShell. Pastikan server tetap berjalan di terminal pertama.

### A. GET seluruh Matakuliah — HTTP 200

```powershell
python -c "import requests; r=requests.get('http://localhost:6543/api/matakuliah'); print(r.status_code); print(r.text)"
```

### B. GET detail Matakuliah — HTTP 200 atau 404

```powershell
python -c "import requests; r=requests.get('http://localhost:6543/api/matakuliah/1'); print(r.status_code); print(r.text)"
```

### C. POST tambah Matakuliah — HTTP 201

```powershell
python -c "import requests; r=requests.post('http://localhost:6543/api/matakuliah', json={'kode_mk':'IF2150','nama_mk':'Pemrograman Berorientasi Objek','sks':3,'semester':5}); print(r.status_code); print(r.text)"
```

Gunakan kode yang belum ada. ID data baru akan terlihat di response.

### D. PUT ubah Matakuliah — HTTP 200

Ganti `4` dengan ID yang dikembalikan oleh POST.

```powershell
python -c "import requests; r=requests.put('http://localhost:6543/api/matakuliah/4', json={'kode_mk':'IF2150','nama_mk':'Pemrograman Berorientasi Objek Lanjut','sks':4,'semester':6}); print(r.status_code); print(r.text)"
```

### E. DELETE Matakuliah — HTTP 200

Ganti `4` dengan ID yang ingin dihapus.

```powershell
python -c "import requests; r=requests.delete('http://localhost:6543/api/matakuliah/4'); print(r.status_code); print(r.text)"
```

### F. Uji validasi dan error

Contoh mengirim SKS negatif. Hasil yang diharapkan adalah **HTTP 400** dengan pesan bahwa SKS harus integer positif:

```powershell
python -c "import requests; r=requests.post('http://localhost:6543/api/matakuliah', json={'kode_mk':'IF2198','nama_mk':'Mata Kuliah Uji','sks':-1,'semester':5}); print(r.status_code); print(r.text)"
```

Skenario validasi lainnya:

| Tujuan pengujian | Hasil yang diharapkan |
|---|---|
| GET ID yang tidak ditemukan | HTTP 404, `Matakuliah tidak ditemukan` |
| POST tanpa satu atau lebih field wajib | HTTP 400, field wajib disebutkan |
| POST dengan kode MK yang sudah dipakai | HTTP 400, kode mata kuliah sudah digunakan |
| POST dengan SKS negatif atau nol | HTTP 400, SKS harus integer positif |
| POST dengan semester nol atau negatif | HTTP 400, semester harus integer positif |
| PUT dengan SKS/semester tidak valid | HTTP 400, pesan validasi terkait |
| DELETE ID yang tidak ditemukan | HTTP 404, `Matakuliah tidak ditemukan` |

## Pengujian Otomatis

Setelah PostgreSQL berjalan, migrasi diterapkan, dan `DATABASE_URL` disetel pada PowerShell yang sama:

```powershell
python -m pytest -q
```

Pengujian mencakup validasi dan operasi Matakuliah serta beberapa endpoint Mahasiswa untuk memastikan modul sebelumnya tetap berfungsi. Saat menulis README ini, rangkaian pengujian dijalankan pada PostgreSQL lokal: **16 passed**. Pyramid juga menampilkan warning deprecation `pkg_resources` dari dependency; warning tersebut tidak menghentikan test.

## Bukti Screenshot Pengujian

Screenshot yang sudah diambil dari terminal dan dimasukkan ke repository:

### GET seluruh Matakuliah

![Hasil GET seluruh Matakuliah](screenshots/01-get-matakuliah.png)

### POST Matakuliah

![Hasil POST Matakuliah](screenshots/02-post-matakuliah.png)

### PUT Matakuliah

![Hasil PUT Matakuliah](screenshots/03-put-matakuliah.png)

### DELETE Matakuliah

![Hasil DELETE Matakuliah](screenshots/04-delete-matakuliah.png)

### Validasi SKS negatif

![Hasil validasi SKS negatif](screenshots/05-validasi-matakuliah.png)

Screenshot tambahan untuk hasil `pytest` dan endpoint Mahasiswa belum dimasukkan. Kalau sudah diambil, simpan sebagai `screenshots/06-pytest.png` dan `screenshots/07-mahasiswa-api.png`, lalu tambahkan link gambarnya di bagian ini.

## Catatan Implementasi

- `Matakuliah` memakai `Base` yang sama dengan model Mahasiswa. `to_dict()` mengembalikan semua kolom untuk response JSON.
- Validator model dan controller memastikan `sks` serta `semester` merupakan integer positif; boolean juga ditolak walaupun di Python `bool` merupakan turunan `int`.
- Route menggunakan URL Dispatch Pyramid dengan predikat method HTTP, sehingga endpoint list dan detail tidak tertukar.
- Controller memakai `request.dbsession`, mengecek kode mata kuliah duplikat, dan melakukan rollback ketika terjadi error database.
- Alembic membaca metadata dari `pyramid_mahasiswa.models`; file migrasi dibuat dengan `--autogenerate`, bukan ditulis manual.
- `.gitignore` mengecualikan virtual environment, cache, database lokal, dan konfigurasi environment berisi kredensial.
