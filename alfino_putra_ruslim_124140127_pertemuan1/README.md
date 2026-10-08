# KantinKu Mini POS

Aplikasi Kasir & Keranjang Belanja Sederhana untuk studi kasus kantin atau toko kampus.

## Identitas

- **Nama:** Alfino Putra Ruslim
- **NIM:** 124140127
- **Kelas praktikum:** RA
- **Pertemuan:** 1 — JavaScript Dasar

## Deskripsi Aplikasi

KantinKu adalah aplikasi web kasir satu halaman yang membantu kasir menambahkan barang, melihat daftar belanja, menghitung subtotal dan total transaksi, menerapkan diskon, serta menghitung kembalian. Aplikasi dibuat menggunakan HTML, CSS, dan JavaScript murni tanpa framework agar konsep DOM, event handler, array/object, validasi form, dan `localStorage` terlihat jelas.

## Struktur Folder

```text
alfino_putra_ruslim_124140127_pertemuan1/
├── index.html
├── style.css
├── script.js
├── README.md
└── modul/
    └── latihan-jsdasar.js
```

## Fitur

- [x] Validasi nama barang minimal 3 karakter.
- [x] Validasi harga berupa angka minimal Rp 500.
- [x] Validasi qty berupa bilangan bulat minimal 1.
- [x] Pesan error berwarna merah di bawah field yang bermasalah.
- [x] Form otomatis di-reset setelah barang berhasil ditambahkan.
- [x] Tabel keranjang dengan nomor, nama, harga satuan, qty, subtotal, dan aksi.
- [x] Subtotal otomatis dari harga satuan dikali qty.
- [x] Total belanja otomatis menggunakan akumulasi seluruh subtotal.
- [x] Diskon otomatis 10% untuk total belanja minimal Rp 50.000.
- [x] Kode promo `HEMAT10` sebagai alternatif pengaktif diskon.
- [x] Perhitungan kembalian dan notifikasi ketika uang belum mencukupi.
- [x] Hapus item dan hitung ulang ringkasan secara real-time.
- [x] Penyimpanan keranjang persisten menggunakan `JSON.stringify()` dan `JSON.parse()`.
- [x] Tombol transaksi baru untuk mengosongkan keranjang dan `localStorage`.
- [x] Layout responsif untuk desktop, tablet, dan mobile.
- [x] Label form, focus state keyboard, dan `aria-live` untuk feedback transaksi.

## Panduan Menjalankan

1. Buka folder `alfino_putra_ruslim_124140127_pertemuan1` di VS Code.
2. Jalankan `index.html` menggunakan ekstensi **Live Server**, atau buka file tersebut langsung di browser modern.
3. Isi nama barang, harga satuan, dan qty, lalu klik **Tambahkan ke keranjang**.
4. Tambahkan barang lain untuk melihat akumulasi total dan diskon otomatis.
5. Isi **Nominal uang bayar** untuk melihat kembalian.
6. Refresh halaman untuk memastikan isi keranjang tetap tersimpan.

Aplikasi memerlukan browser yang mendukung JavaScript modern dan `localStorage` (Chrome, Edge, Firefox, atau Safari versi terbaru).

## Penjelasan Teknis Singkat

### Validasi input

Event `submit` pada form dicegah dengan `event.preventDefault()`. Fungsi `validateProduct()` membersihkan nama, mengubah harga dan qty menjadi angka, lalu memeriksa seluruh aturan. Jika ada kesalahan, class `input-invalid`, atribut `aria-invalid`, dan pesan error dipasang pada field terkait. Barang hanya dibuat dan dimasukkan ke array `cart` apabila semua validasi lolos.

### Perhitungan transaksi

Fungsi `calculateSummary()` menggunakan `reduce()` untuk menjumlahkan `price * quantity` setiap item. Jika subtotal minimal Rp 50.000 atau kode `HEMAT10` aktif, diskon dihitung sebesar 10%. Total akhir adalah subtotal dikurangi diskon. Fungsi `updatePayment()` membandingkan nominal pembayaran dengan total akhir, lalu menampilkan keterangan uang kurang atau nilai kembalian.

### LocalStorage

Setiap perubahan array keranjang memanggil `saveCart()`, yang menyimpan data dengan `localStorage.setItem(STORAGE_KEY, JSON.stringify(cart))`. Saat halaman dibuka, `loadCart()` mengambil string tersebut dan mengubahnya kembali menjadi array memakai `JSON.parse()`. Tombol **Transaksi baru** menghapus array dan memanggil `localStorage.removeItem(STORAGE_KEY)`.

## Tangkapan Layar untuk Laporan

Ambil minimal tiga screenshot setelah menjalankan aplikasi dan lampirkan pada laporan praktikum:

1. **Tampilan utama:** form input barang dan keranjang kosong.
2. **Tampilan validasi:** klik tombol tambah dengan field kosong atau data tidak sesuai sehingga pesan merah terlihat.
3. **Tampilan hasil transaksi:** beberapa barang, tabel keranjang, diskon, total akhir, dan kembalian terlihat.

Disarankan memberi nama file `01-form-utama.png`, `02-validasi-error.png`, dan `03-hasil-transaksi.png` agar mudah dirujuk pada laporan.

## Referensi Materi

Implementasi mengikuti materi Pertemuan 1 JavaScript Dasar: variabel dan kondisional, loop dan fungsi, array dan objek, manipulasi DOM, event handler, validasi form, serta penggunaan `localStorage`.

## Catatan Pengumpulan

Repository GitHub yang disarankan mengikuti format `pemrograman_web_itera_124140127` dan dibuat **Public**. Kelas praktikum: **RA**. Deadline pengumpulan sesuai instruksi adalah Sabtu, 10 Oktober 2026 pukul 23.59 WIB.
