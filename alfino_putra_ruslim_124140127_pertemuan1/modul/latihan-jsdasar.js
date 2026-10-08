// Dokumentasi latihan Pertemuan 1: JavaScript Dasar
// Identitas: Alfino Putra Ruslim - 124140127

const mahasiswa = {
  nama: "Alfino Putra Ruslim",
  nim: "124140127",
  kelas: "Belum diisi"
};

const nilai = [85, 92, 78, 90, 88];
const totalNilai = nilai.reduce((total, item) => total + item, 0);
const rataRata = totalNilai / nilai.length;

function kategoriNilai(score) {
  if (score >= 90) return "A";
  if (score >= 80) return "B";
  if (score >= 70) return "C";
  return "D";
}

function fizzBuzz(batas) {
  const hasil = [];
  for (let angka = 1; angka <= batas; angka += 1) {
    if (angka % 15 === 0) hasil.push("FizzBuzz");
    else if (angka % 3 === 0) hasil.push("Fizz");
    else if (angka % 5 === 0) hasil.push("Buzz");
    else hasil.push(angka);
  }
  return hasil;
}

console.log("Mahasiswa:", mahasiswa);
console.log("Rata-rata nilai:", rataRata.toFixed(2));
console.log("Grade nilai pertama:", kategoriNilai(nilai[0]));
console.log("Contoh FizzBuzz 1-15:", fizzBuzz(15));
