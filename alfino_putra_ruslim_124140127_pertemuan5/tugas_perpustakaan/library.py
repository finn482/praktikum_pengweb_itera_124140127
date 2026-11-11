"""Class pengelola koleksi perpustakaan."""


class Library:
    """Menyimpan dan mengelola item perpustakaan secara terpusat."""

    def __init__(self, nama):
        """Membuat perpustakaan dengan koleksi privat yang masih kosong."""
        self.nama = nama
        self.__koleksi = []

    @property
    def jumlah_item(self):
        """Mengembalikan jumlah item yang terdaftar di perpustakaan."""
        return len(self.__koleksi)

    def tambah_item(self, item):
        """Menambahkan item baru jika ID-nya belum dipakai.

        Returns:
            bool: True jika berhasil ditambahkan, False jika ID duplikat.
        """
        if self.cari_item(item.id_item):
            return False
        self.__koleksi.append(item)
        return True

    def tampilkan_katalog(self, hanya_tersedia=False):
        """Menghasilkan daftar detail item yang ada di katalog.

        Args:
            hanya_tersedia (bool): Jika True, hanya item yang belum dipinjam.

        Returns:
            list: List string detail item.
        """
        daftar_item = self.__koleksi
        if hanya_tersedia:
            daftar_item = [item for item in daftar_item if not item.is_dipinjam]
        return [item.get_detail() for item in daftar_item]

    def cari_item(self, kata_kunci):
        """Mencari item berdasarkan ID atau bagian dari judul.

        Args:
            kata_kunci (str): ID atau teks judul yang ingin dicari.

        Returns:
            list: List objek item yang sesuai dengan kata kunci.
        """
        kata_kunci = str(kata_kunci).lower()
        return [
            item
            for item in self.__koleksi
            if kata_kunci in item.id_item.lower() or kata_kunci in item.judul.lower()
        ]

    def pinjam_item(self, id_item):
        """Meminjam item berdasarkan ID.

        Returns:
            object | None: Item yang berhasil dipinjam atau None jika gagal.
        """
        item = self._ambil_berdasarkan_id(id_item)
        if item and item.pinjam():
            return item
        return None

    def kembalikan_item(self, id_item):
        """Mengembalikan item berdasarkan ID.

        Returns:
            object | None: Item yang berhasil dikembalikan atau None jika gagal.
        """
        item = self._ambil_berdasarkan_id(id_item)
        if item and item.kembalikan():
            return item
        return None

    def _ambil_berdasarkan_id(self, id_item):
        """Mencari satu item berdasarkan ID secara internal."""
        return next((item for item in self.__koleksi if item.id_item == id_item), None)
