"""Program utama untuk mencoba modul math_operations."""

import math_operations
from math_operations import (
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    keliling_persegi,
    luas_persegi_panjang,
)


def cetak_bagian(judul):
    """Mencetak judul bagian output program.

    Args:
        judul (str): Nama bagian yang ingin ditampilkan.

    Returns:
        None: Fungsi hanya mencetak teks ke terminal.
    """
    print(f"\n--- {judul} ---")


def main():
    """Menjalankan semua fungsi geometri dan konversi temperatur."""
    print("=" * 52)
    print("       DEMO MODUL MATEMATIKA PYTHON")
    print("=" * 52)

    cetak_bagian("PERSEGI")
    sisi = 6
    print(f"Sisi                  : {sisi}")
    print(f"Luas                  : {math_operations.luas_persegi(sisi):.2f}")
    print(f"Keliling              : {keliling_persegi(sisi):.2f}")

    cetak_bagian("PERSEGI PANJANG")
    panjang, lebar = 10, 4
    print(f"Panjang x lebar       : {panjang} x {lebar}")
    print(f"Luas                  : {luas_persegi_panjang(panjang, lebar):.2f}")
    print(
        f"Keliling              : "
        f"{math_operations.keliling_persegi_panjang(panjang, lebar):.2f}"
    )

    cetak_bagian("LINGKARAN")
    jari_jari = 7
    print(f"Jari-jari             : {jari_jari}")
    print(f"Konstanta PI          : {math_operations.PI}")
    print(f"Luas                  : {math_operations.luas_lingkaran(jari_jari):.2f}")
    print(f"Keliling              : {math_operations.keliling_lingkaran(jari_jari):.2f}")

    cetak_bagian("KONVERSI TEMPERATUR")
    celsius = 25
    print(f"Celsius               : {celsius:.2f} °C")
    print(f"Fahrenheit            : {celsius_to_fahrenheit(celsius):.2f} °F")
    print(f"Kelvin                : {celsius_to_kelvin(celsius):.2f} K")


if __name__ == "__main__":
    main()
