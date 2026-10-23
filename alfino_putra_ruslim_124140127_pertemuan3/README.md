# Sudut Baca — Aplikasi Manajemen Buku Pribadi

Sudut Baca adalah aplikasi React sederhana untuk mencatat buku yang sudah dimiliki, sedang dibaca, atau ingin dibeli. Aplikasi ini saya buat karena daftar buku biasanya cepat tercecer kalau hanya dicatat di notes. Dengan dashboard ini, status koleksi bisa dilihat dan diperbarui dari satu tempat.

## Identitas

- **Nama:** Alfino Putra Ruslim
- **NIM:** 124140127
- **Kelas:** RA
- **Pertemuan:** 3 — React dan Manajemen State

## Fitur Aplikasi

- Tambah buku dengan judul, penulis, status, dan catatan.
- Edit detail buku.
- Hapus buku dengan konfirmasi.
- Tandai buku selesai dibaca atau kembalikan ke status belum selesai.
- Filter berdasarkan status: semua, sudah punya, sedang baca, dan ingin beli.
- Pencarian berdasarkan judul atau penulis.
- Halaman statistik koleksi buku melalui React Router.
- Data tetap tersimpan setelah browser di-refresh menggunakan `localStorage`.
- Feedback error ketika judul atau penulis belum diisi.
- Tampilan responsif untuk desktop dan layar kecil.

## Teknologi yang Dipakai

- React 19 dengan functional components dan Hooks.
- Vite sebagai build tool.
- React Router untuk halaman Koleksi dan Statistik.
- Context API untuk state buku.
- PropTypes untuk validasi props komponen.
- Vitest dan React Testing Library untuk unit test.
- CSS biasa dengan pendekatan komponen agar tidak bergantung pada framework UI.

## Struktur Folder

```text
alfino_putra_ruslim_124140127_pertemuan3/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── App.jsx
    ├── App.css
    ├── index.css
    ├── components/
    │   ├── BookCard/
    │   ├── BookFilter/
    │   ├── BookForm/
    │   └── BookList/
    ├── context/
    │   └── BookContext.jsx
    ├── hooks/
    │   ├── useBookStats.js
    │   └── useLocalStorage.js
    ├── pages/
    │   ├── Home/
    │   └── Stats/
    └── test/
        ├── app.test.jsx
        └── setup.js
```

## Instalasi dan Menjalankan

Pastikan Node.js sudah terpasang, kemudian jalankan dari folder project:

```bash
npm install
npm run dev
```

Buka URL yang muncul di terminal, biasanya `http://localhost:5173`.

Perintah lain yang tersedia:

```bash
npm run build    # membuat build production
npm run lint     # memeriksa masalah lint
npm test         # menjalankan unit test sekali
npm run test:watch
```

## Penjelasan Implementasi React

### `useState` dan `useEffect`

`BookForm` menggunakan `useState` untuk nilai input dan pesan validasi. `useEffect` dipakai untuk mengisi ulang form ketika mode edit menerima buku yang berbeda. Hook `useLocalStorage` juga memakai `useEffect` untuk menyimpan perubahan state ke browser.

### Context API

`BookProvider` pada `src/context/BookContext.jsx` menjadi tempat state utama. Fungsi `addBook`, `updateBook`, `removeBook`, dan `toggleFinished` dibagikan melalui `useBooks()`, sehingga komponen kartu dan form tidak perlu menerima terlalu banyak prop.

### React Router

`App.jsx` menggunakan `BrowserRouter`, `Routes`, dan `Route`. Halaman `/` berisi koleksi buku, sedangkan `/stats` berisi statistik. Navigasi dilakukan memakai `NavLink` dan `Link`.

### Custom hooks

- `useLocalStorage.js` menangani baca/tulis JSON secara persisten dan memiliki fallback jika browser menolak akses storage.
- `useBookStats.js` menghitung total koleksi, jumlah status, jumlah buku selesai, dan persentase progres memakai `useMemo`.

### Komponen reusable

`BookForm`, `BookFilter`, `BookList`, dan `BookCard` dipisahkan agar setiap komponen memiliki tanggung jawab yang jelas. Props utama pada komponen-komponen tersebut dilengkapi `PropTypes`.

## Testing

Terdapat 7 unit test pada `src/test/app.test.jsx`, yaitu:

1. Menghitung statistik buku dengan custom hook.
2. Memanggil callback pencarian.
3. Memanggil callback filter status.
4. Menampilkan error form ketika input kosong.
5. Menyimpan buku baru setelah form valid.
6. Menampilkan metadata dan aksi edit pada kartu buku.
7. Mengubah status buku menjadi selesai.

Jalankan dengan:

```bash
npm test
```

Untuk laporan praktikum, simpan screenshot output terminal Vitest sebagai `testing-result.png` di folder `screenshots/` jika screenshot sudah diambil.

## Screenshot Antarmuka

Screenshot aplikasi dan hasil eksekusi test dapat ditambahkan ke folder `screenshots/` dengan nama berikut:

- `01-koleksi-buku.png` — halaman koleksi utama.
- `02-form-validasi.png` — feedback error ketika judul/penulis kosong.
- `03-halaman-statistik.png` — halaman ringkasan koleksi.
- `testing-result.png` — hasil `npm test` di terminal.

Screenshot perlu diambil setelah menjalankan aplikasi di browser dan unit test di terminal. Saya tidak menambahkan gambar contoh yang bukan hasil dari project ini agar dokumentasinya tetap sesuai kondisi aplikasi sebenarnya.

## Catatan Kode

Komentar singkat ditempatkan pada bagian yang menjelaskan tanggung jawab khusus, seperti sinkronisasi `localStorage`, Context API, dan validasi form. Nama fungsi dan state dibuat cukup deskriptif supaya alurnya mudah diikuti saat praktikum.
