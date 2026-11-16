"""Model ORM Matakuliah."""

from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, validates

from .meta import Base


class Matakuliah(Base):
    """Merepresentasikan data mata kuliah pada tabel matakuliah."""

    __tablename__ = "matakuliah"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kode_mk: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    nama_mk: Mapped[str] = mapped_column(Text, nullable=False)
    sks: Mapped[int] = mapped_column(Integer, nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)

    @validates("sks", "semester")
    def validate_positive_integer(self, key, value):
        """Memastikan SKS dan semester berupa integer positif."""
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"{key} harus berupa integer positif")
        return value

    def to_dict(self):
        """Mengubah model Matakuliah menjadi dictionary JSON serializable."""
        return {
            "id": self.id,
            "kode_mk": self.kode_mk,
            "nama_mk": self.nama_mk,
            "sks": self.sks,
            "semester": self.semester,
        }
