"""Model item perpustakaan dan subclass turunannya."""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Abstract class dasar untuk semua item yang ada di perpustakaan."""

    def __init__(self, id_item, judul):
        """Menyimpan identitas item dan status peminjamannya."""
        self._id_item = id_item
        self._judul = judul
        self._is_dipinjam = False

    @property
    def id_item(self):
        """Mengembalikan ID item sebagai atribut yang hanya bisa dibaca."""
        return self._id_item

    @property
    def judul(self):
        """Mengembalikan judul item sebagai atribut yang hanya bisa dibaca."""
        return self._judul

    @property
    def is_dipinjam(self):
        """Mengembalikan status peminjaman item."""
        return self._is_dipinjam

    def pinjam(self):
        """Mengubah status item menjadi sedang dipinjam."""
        if self._is_dipinjam:
            return False
        self._is_dipinjam = True
        return True

    def kembalikan(self):
        """Mengubah status item menjadi tersedia kembali."""
        if not self._is_dipinjam:
            return False
        self._is_dipinjam = False
        return True

    @abstractmethod
    def get_detail(self):
        """Menghasilkan detail item dalam format teks."""
        raise NotImplementedError

    @abstractmethod
    def hitung_denda(self, hari_terlambat):
        """Menghitung denda berdasarkan jumlah hari keterlambatan."""
        raise NotImplementedError

    def __str__(self):
        """Mengembalikan detail item agar nyaman ditampilkan dengan print."""
        return self.get_detail()


class Book(LibraryItem):
    """Item buku dengan penulis dan jumlah halaman."""

    def __init__(self, id_item, judul, penulis, jumlah_halaman):
        """Membuat objek buku dan mengisi data spesifik buku."""
        super().__init__(id_item, judul)
        self._penulis = penulis
        self._jumlah_halaman = jumlah_halaman

    def get_detail(self):
        """Menghasilkan detail buku untuk katalog perpustakaan."""
        status = "Dipinjam" if self.is_dipinjam else "Tersedia"
        return (
            f"[{self.id_item}] {self.judul} | Buku | Penulis: {self._penulis} "
            f"| {self._jumlah_halaman} halaman | {status}"
        )

    def hitung_denda(self, hari_terlambat):
        """Menghitung denda buku sebesar Rp2.000 per hari keterlambatan."""
        return max(0, hari_terlambat) * 2_000


class Magazine(LibraryItem):
    """Item majalah dengan nomor edisi dan periode terbit."""

    def __init__(self, id_item, judul, edisi, periode_terbit):
        """Membuat objek majalah dan mengisi data edisinya."""
        super().__init__(id_item, judul)
        self._edisi = edisi
        self._periode_terbit = periode_terbit

    def get_detail(self):
        """Menghasilkan detail majalah untuk katalog perpustakaan."""
        status = "Dipinjam" if self.is_dipinjam else "Tersedia"
        return (
            f"[{self.id_item}] {self.judul} | Majalah | Edisi: {self._edisi} "
            f"| Terbit: {self._periode_terbit} | {status}"
        )

    def hitung_denda(self, hari_terlambat):
        """Menghitung denda majalah sebesar Rp1.000 per hari keterlambatan."""
        return max(0, hari_terlambat) * 1_000
