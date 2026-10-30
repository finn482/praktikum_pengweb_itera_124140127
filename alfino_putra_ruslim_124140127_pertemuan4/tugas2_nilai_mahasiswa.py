"""Program pengelolaan nilai mahasiswa menggunakan list dan dictionary."""

DATA_MAHASISWA = [
    {"nama": "Alfino Putra Ruslim", "nim": "124140127", "nilai_uts": 82, "nilai_uas": 88, "nilai_tugas": 90},
    {"nama": "Nadia Prameswari", "nim": "124140128", "nilai_uts": 76, "nilai_uas": 81, "nilai_tugas": 85},
    {"nama": "Raka Aditya", "nim": "124140129", "nilai_uts": 68, "nilai_uas": 72, "nilai_tugas": 70},
    {"nama": "Salsa Maharani", "nim": "124140130", "nilai_uts": 55, "nilai_uas": 60, "nilai_tugas": 58},
    {"nama": "Dimas Pratama", "nim": "124140131", "nilai_uts": 42, "nilai_uas": 48, "nilai_tugas": 45},
]


def hitung_nilai_akhir(nilai_uts, nilai_uas, nilai_tugas):
    """Menghitung nilai akhir dengan bobot UTS 30%, UAS 40%, dan tugas 30%.

    Args:
        nilai_uts (float): Nilai ujian tengah semester.
        nilai_uas (float): Nilai ujian akhir semester.
        nilai_tugas (float): Nilai tugas.

    Returns:
        float: Nilai akhir mahasiswa.
    """
    return (0.30 * nilai_uts) + (0.40 * nilai_uas) + (0.30 * nilai_tugas)


def tentukan_grade(nilai_akhir):
    """Menentukan grade A sampai E berdasarkan nilai akhir.

    Args:
        nilai_akhir (float): Nilai akhir mahasiswa.

    Returns:
        str: Grade akademik mahasiswa.
    """
    if nilai_akhir >= 80:
        return "A"
    if nilai_akhir >= 70:
        return "B"
    if nilai_akhir >= 60:
        return "C"
    if nilai_akhir >= 50:
        return "D"
    return "E"


def lengkapi_data_mahasiswa(mahasiswa):
    """Menambahkan nilai akhir dan grade ke dictionary mahasiswa.

    Args:
        mahasiswa (dict): Data mahasiswa dan nilai komponennya.

    Returns:
        dict: Dictionary mahasiswa yang sudah dilengkapi hasil perhitungan.
    """
    nilai_akhir = hitung_nilai_akhir(
        mahasiswa["nilai_uts"], mahasiswa["nilai_uas"], mahasiswa["nilai_tugas"]
    )
    return {**mahasiswa, "nilai_akhir": nilai_akhir, "grade": tentukan_grade(nilai_akhir)}


def cetak_tabel(data_mahasiswa):
    """Mencetak data mahasiswa dalam bentuk tabel berkolom.

    Args:
        data_mahasiswa (list): List dictionary data mahasiswa lengkap.

    Returns:
        None: Fungsi hanya mencetak tabel ke terminal.
    """
    header = f"{'Nama':<23} {'NIM':<11} {'UTS':>6} {'UAS':>6} {'Tugas':>7} {'Akhir':>8} {'Grade':>6}"
    print(header)
    print("-" * len(header))
    for mahasiswa in data_mahasiswa:
        print(
            f"{mahasiswa['nama']:<23} {mahasiswa['nim']:<11} "
            f"{mahasiswa['nilai_uts']:>6.1f} {mahasiswa['nilai_uas']:>6.1f} "
            f"{mahasiswa['nilai_tugas']:>7.1f} {mahasiswa['nilai_akhir']:>8.2f} "
            f"{mahasiswa['grade']:>6}"
        )


def tampilkan_ekstrem(data_mahasiswa):
    """Menampilkan mahasiswa dengan nilai akhir tertinggi dan terendah.

    Args:
        data_mahasiswa (list): List dictionary mahasiswa yang sudah dihitung.

    Returns:
        None: Fungsi mencetak dua data ekstrem ke terminal.
    """
    tertinggi = max(data_mahasiswa, key=lambda mahasiswa: mahasiswa["nilai_akhir"])
    terendah = min(data_mahasiswa, key=lambda mahasiswa: mahasiswa["nilai_akhir"])
    print("\nRingkasan Nilai")
    print("-" * 42)
    print(f"Nilai tertinggi: {tertinggi['nama']} ({tertinggi['nilai_akhir']:.2f})")
    print(f"Nilai terendah : {terendah['nama']} ({terendah['nilai_akhir']:.2f})")


def main():
    """Menjalankan perhitungan dan menampilkan rekap nilai mahasiswa."""
    data_lengkap = [lengkapi_data_mahasiswa(mahasiswa) for mahasiswa in DATA_MAHASISWA]
    print("=" * 82)
    print("                 REKAP NILAI MAHASISWA")
    print("=" * 82)
    cetak_tabel(data_lengkap)
    tampilkan_ekstrem(data_lengkap)


if __name__ == "__main__":
    main()
