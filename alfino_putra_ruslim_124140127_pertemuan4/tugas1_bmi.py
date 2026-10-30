"""Program penghitung BMI sederhana untuk tugas Pertemuan 4."""


def hitung_bmi(berat_badan, tinggi_badan):
    """Menghitung BMI dari berat dalam kg dan tinggi dalam meter.

    Args:
        berat_badan (float): Berat badan dalam kilogram.
        tinggi_badan (float): Tinggi badan dalam meter.

    Returns:
        float: Nilai BMI.

    Raises:
        ValueError: Jika berat atau tinggi tidak bernilai positif.
    """
    if berat_badan <= 0 or tinggi_badan <= 0:
        raise ValueError("Berat dan tinggi harus lebih besar dari nol.")
    return berat_badan / (tinggi_badan * tinggi_badan)


def tentukan_kategori_bmi(nilai_bmi):
    """Menentukan kategori berat badan berdasarkan nilai BMI.

    Args:
        nilai_bmi (float): Nilai BMI yang sudah dihitung.

    Returns:
        str: Kategori berat badan.
    """
    if nilai_bmi < 18.5:
        return "Berat badan kurang"
    if nilai_bmi < 25:
        return "Berat badan normal"
    if nilai_bmi < 30:
        return "Berat badan berlebih"
    return "Obesitas"


def minta_angka_positif(label):
    """Meminta input angka positif dari pengguna.

    Args:
        label (str): Teks petunjuk yang ditampilkan di terminal.

    Returns:
        float: Angka positif hasil input pengguna.
    """
    while True:
        try:
            nilai = float(input(label))
            if nilai <= 0:
                print("Input harus lebih besar dari nol. Coba lagi.")
                continue
            return nilai
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")


def main():
    """Menjalankan alur input, perhitungan, dan output program BMI."""
    print("=" * 42)
    print("       PROGRAM PENGHITUNG BMI")
    print("=" * 42)
    berat_badan = minta_angka_positif("Masukkan berat badan (kg): ")
    tinggi_badan = minta_angka_positif("Masukkan tinggi badan (m): ")
    nilai_bmi = hitung_bmi(berat_badan, tinggi_badan)
    kategori = tentukan_kategori_bmi(nilai_bmi)

    print("\nHasil Perhitungan")
    print("-" * 42)
    print(f"Berat badan : {berat_badan:.2f} kg")
    print(f"Tinggi badan: {tinggi_badan:.2f} m")
    print(f"Nilai BMI   : {nilai_bmi:.2f}")
    print(f"Kategori    : {kategori}")


if __name__ == "__main__":
    main()
