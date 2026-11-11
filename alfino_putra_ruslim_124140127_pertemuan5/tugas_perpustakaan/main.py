"""Skrip utama untuk mendemonstrasikan sistem perpustakaan."""

from library import Library
from library_item import Book, Magazine
from member import Member


def tampilkan_hasil_pencarian(library, kata_kunci):
    """Menampilkan hasil pencarian item berdasarkan kata kunci."""
    hasil = library.cari_item(kata_kunci)
    print(f"\nPencarian: '{kata_kunci}'")
    if not hasil:
        print("Tidak ada item yang cocok.")
        return
    for item in hasil:
        print(f"- {item.get_detail()}")


def main():
    """Menjalankan demo tambah item, katalog, pencarian, dan peminjaman."""
    perpustakaan = Library("Perpustakaan Sudut Baca")
    anggota = Member("M-001", "Alfino Putra Ruslim")

    buku_1 = Book("B001", "Laskar Pelangi", "Andrea Hirata", 529)
    buku_2 = Book("B002", "Filosofi Teras", "Henry Manampiring", 346)
    majalah_1 = Magazine("M001", "National Geographic", "Edisi 08", "Agustus 2026")

    print("=" * 76)
    print(f"          {perpustakaan.nama.upper()}")
    print("=" * 76)
    print("\n[1] Menambahkan item")
    for item in (buku_1, buku_2, majalah_1):
        berhasil = perpustakaan.tambah_item(item)
        status = "berhasil" if berhasil else "gagal"
        print(f"- Tambah {item.judul:<25} [{item.id_item}]: {status}")

    print("\n[2] Katalog semua item")
    for detail in perpustakaan.tampilkan_katalog():
        print(f"- {detail}")

    tampilkan_hasil_pencarian(perpustakaan, "B002")
    tampilkan_hasil_pencarian(perpustakaan, "National")

    print("\n[3] Demonstrasi peminjaman")
    item_dipinjam = perpustakaan.pinjam_item("B001")
    if item_dipinjam:
        anggota.tambah_pinjaman(item_dipinjam)
        print(f"{anggota.nama} meminjam: {item_dipinjam.judul}")
        print(f"Jumlah pinjaman anggota: {anggota.jumlah_pinjaman}")

    print("\nKatalog item yang tersedia setelah peminjaman:")
    for detail in perpustakaan.tampilkan_katalog(hanya_tersedia=True):
        print(f"- {detail}")

    print("\n[4] Polymorphism: denda tiap subclass")
    for item in (buku_1, majalah_1):
        print(f"- {item.judul:<25} | Denda 3 hari: Rp{item.hitung_denda(3):,}")

    print("\n[5] Pengembalian item")
    dikembalikan = perpustakaan.kembalikan_item("B001")
    if dikembalikan:
        anggota.hapus_pinjaman(dikembalikan)
        print(f"{dikembalikan.judul} sudah dikembalikan.")
    print(f"Daftar pinjaman {anggota.nama}: {anggota.tampilkan_pinjaman() or 'Tidak ada'}")


if __name__ == "__main__":
    main()
