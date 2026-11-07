# Tugas Dasar Pemrograman Python — Pertemuan 4

## Identitas

- **Nama:** Alfino Putra Ruslim
- **NIM:** 124140127
- **Kelas:** RA

## Deskripsi Tugas

Pada tugas ini saya membuat tiga program Python untuk menerapkan materi dasar yang sudah dipelajari, yaitu variabel, percabangan, perulangan, fungsi, list, dictionary, dan modul Python.

Program pertama digunakan untuk menghitung BMI. Program kedua digunakan untuk mengolah nilai beberapa mahasiswa dan menentukan grade masing-masing. Program ketiga berisi modul matematika buatan sendiri yang dipanggil dari `main.py`.

Semua program dibuat tanpa library tambahan. Setiap fungsi juga diberi docstring supaya tujuan, parameter, dan hasil kembaliannya lebih jelas.

## Struktur Folder

```text
alfino_putra_ruslim_124140127_pertemuan4/
├── .gitignore
├── README.md
├── tugas1_bmi.py
├── tugas2_nilai_mahasiswa.py
├── math_operations.py
├── main.py
└── screenshots/
    ├── soal1-bmi.png
    ├── soal2-nilai-mahasiswa.png
    └── soal3-modul-matematika.png
```

Folder `venv/`, `.venv/`, `__pycache__/`, dan file bytecode Python sudah dimasukkan ke `.gitignore`, jadi tidak ikut diunggah ke Git.

## Penjelasan Program

### 1. Program Penghitung BMI — `tugas1_bmi.py`

Program meminta berat badan dalam kilogram dan tinggi badan dalam meter. Nilai BMI dihitung menggunakan rumus:

```text
BMI = berat badan / (tinggi badan × tinggi badan)
```

Setelah nilai BMI didapatkan, program menggunakan percabangan `if-elif-else` untuk menentukan kategori berat badan:

- BMI kurang dari 18.5: Berat badan kurang.
- BMI 18.5 sampai kurang dari 25: Berat badan normal.
- BMI 25 sampai kurang dari 30: Berat badan berlebih.
- BMI 30 atau lebih: Obesitas.

Program juga melakukan validasi sederhana supaya input berat dan tinggi harus berupa angka positif.

### 2. Program Nilai Mahasiswa — `tugas2_nilai_mahasiswa.py`

Data mahasiswa disimpan dalam sebuah list yang berisi lima dictionary. Setiap dictionary menyimpan nama, NIM, nilai UTS, nilai UAS, dan nilai tugas.

Nilai akhir dihitung dengan bobot:

```text
Nilai akhir = (30% × UTS) + (40% × UAS) + (30% × nilai tugas)
```

Setelah itu, program menentukan grade A sampai E, mencetak data dalam bentuk tabel, serta mencari mahasiswa dengan nilai akhir tertinggi dan terendah.

### 3. Modul Matematika — `math_operations.py` dan `main.py`

File `math_operations.py` berisi konstanta `PI` dan beberapa fungsi, yaitu:

- Luas dan keliling persegi.
- Luas dan keliling persegi panjang.
- Luas dan keliling lingkaran.
- Konversi Celsius ke Fahrenheit.
- Konversi Celsius ke Kelvin.

File `main.py` digunakan untuk memanggil semua fungsi tersebut. Pada file ini saya menerapkan dua cara import modul:

```python
import math_operations
from math_operations import celsius_to_fahrenheit, luas_persegi_panjang
```

## Cara Menjalankan Program di VS Code

1. Pastikan Python sudah terpasang. Cek melalui terminal:

   ```powershell
   python --version
   ```

2. Buka folder `alfino_putra_ruslim_124140127_pertemuan4` di VS Code.
3. Buka terminal PowerShell dengan menu **Terminal → New Terminal**.
4. Jika terminal masih berada di folder repository utama, masuk ke folder tugas:

   ```powershell
   cd .\alfino_putra_ruslim_124140127_pertemuan4
   ```

5. Jalankan program satu per satu.

   Untuk program BMI:

   ```powershell
   python tugas1_bmi.py
   ```

   Untuk program nilai mahasiswa:

   ```powershell
   python tugas2_nilai_mahasiswa.py
   ```

   Untuk program modul matematika:

   ```powershell
   python main.py
   ```

Jika perintah `python` tidak dikenali pada Windows, gunakan perintah `py`, misalnya:

```powershell
py tugas1_bmi.py
```

## Contoh Hasil Program

### Hasil Program BMI

Dengan input berat badan 60 kg dan tinggi badan 1.65 m, hasil yang diperoleh adalah BMI 22.04 dengan kategori berat badan normal.

```text
Nilai BMI   : 22.04
Kategori    : Berat badan normal
```

### Hasil Program Nilai Mahasiswa

Program menampilkan tabel yang berisi nama, NIM, nilai UTS, nilai UAS, nilai tugas, nilai akhir, dan grade. Di bagian bawah tabel terdapat informasi mahasiswa dengan nilai paling tinggi dan paling rendah.

### Hasil Program Modul Matematika

Program menampilkan hasil luas dan keliling dari tiga bentuk geometri, kemudian menampilkan hasil konversi suhu 25°C ke Fahrenheit dan Kelvin.

## Screenshot Hasil Eksekusi

### Soal 1 — Program BMI

Screenshot ini menunjukkan proses input berat dan tinggi badan serta hasil kategori BMI.

![Hasil program BMI](screenshots/soal1-bmi.png)

### Soal 2 — Program Nilai Mahasiswa

Screenshot ini menunjukkan tabel nilai mahasiswa dan informasi nilai tertinggi serta terendah.

![Hasil program nilai mahasiswa](screenshots/soal2-nilai-mahasiswa.png)

### Soal 3 — Modul Matematika

Screenshot ini menunjukkan hasil pemanggilan fungsi geometri dan konversi temperatur dari `main.py`.

![Hasil program modul matematika](screenshots/soal3-modul-matematika.png)

## Penerapan PEP 8

- Indentasi kode menggunakan 4 spasi.
- Nama fungsi dan variabel menggunakan format `snake_case`.
- Setiap fungsi memiliki docstring.
- Setiap program memiliki fungsi `main()` dan pengecekan `if __name__ == "__main__":`.
- Program dipisahkan menjadi beberapa fungsi supaya lebih mudah dibaca dan dirawat.
