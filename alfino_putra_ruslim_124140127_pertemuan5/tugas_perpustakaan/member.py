"""Class anggota perpustakaan dengan enkapsulasi daftar pinjaman."""


class Member:
    """Mewakili anggota yang dapat meminjam item perpustakaan."""

    def __init__(self, id_member, nama):
        """Membuat anggota dengan koleksi pinjaman kosong."""
        self.id_member = id_member
        self.nama = nama
        self.__koleksi_pinjaman = []

    @property
    def jumlah_pinjaman(self):
        """Mengembalikan jumlah item yang sedang dipinjam anggota."""
        return len(self.__koleksi_pinjaman)

    def tambah_pinjaman(self, item):
        """Menyimpan item ke daftar pinjaman privat anggota."""
        if item not in self.__koleksi_pinjaman:
            self.__koleksi_pinjaman.append(item)

    def hapus_pinjaman(self, item):
        """Menghapus item dari daftar pinjaman jika ada."""
        if item in self.__koleksi_pinjaman:
            self.__koleksi_pinjaman.remove(item)

    def tampilkan_pinjaman(self):
        """Mengembalikan daftar judul item yang sedang dipinjam."""
        return [item.judul for item in self.__koleksi_pinjaman]
