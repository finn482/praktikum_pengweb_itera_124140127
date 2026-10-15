# Catatan Modul Pertemuan 2

## Konsep yang dipraktikkan

- `let` dan `const` untuk state yang berubah dan konfigurasi yang tetap.
- Arrow function untuk callback DOM, filter, map, dan handler event.
- Template literals untuk membuat card tugas secara dinamis.
- `async/await` dan `fetch()` untuk mengambil data dari API publik.
- Class `TaskItem` sebagai model data.
- Class `DashboardApp` sebagai pengelola aplikasi.
- Destructuring pada object tugas dan parameter event.
- Spread operator untuk pembaruan state immutable.
- `JSON.stringify()` dan `JSON.parse()` untuk localStorage.

## Alur state

1. `DashboardApp.initialize()` membaca localStorage.
2. Jika belum ada data, aplikasi mengambil data awal dari JSONPlaceholder.
3. Data setiap tugas dibungkus menjadi instance `TaskItem`.
4. Setiap interaksi memperbarui array `tasks` dengan `map`, `filter`, atau spread operator.
5. State disimpan ulang lalu seluruh tampilan dirender kembali.
