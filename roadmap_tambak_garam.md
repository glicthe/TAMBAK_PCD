# Roadmap Penelitian: Preprocessing Citra Satelit untuk Penghitungan Petak Tambak Garam

**Judul kerja:** Pengaruh Preprocessing (Penghilangan Noise, Peningkatan Kontras, dan Sharpening) terhadap Deteksi dan Penghitungan Petak Tambak Garam pada Citra Satelit (Studi Kasus: Madura)

**Pertanyaan penelitian:** Alur preprocessing mana yang paling meningkatkan akurasi penghitungan petak tambak garam?

**Lokasi:** Desa Lembung (Kecamatan Galis, Pamekasan) dan satu desa di Kecamatan Pademawu, Pamekasan.

---

## Ringkasan Tahap

| Tahap | Kegiatan | Hasil |
|---|---|---|
| 1 | Rumuskan masalah dan batas penelitian | Definisi "petak" dan lokasi |
| 2 | Kumpulkan data | 30 sampai 50 tile + log CSV |
| 3 | Siapkan ground truth | Hitungan manual + pembagian tuning/uji |
| 4 | Bangun alur preprocessing | Alur A sampai D |
| 5 | Eksperimen kualitas citra | Tabel PSNR dan SSIM |
| 6 | Bangun metode penghitungan | Pipeline penghitung petak |
| 7 | Jalankan eksperimen utama | Tabel hitungan per alur |
| 8 | Evaluasi | MAE, MAPE, (opsional) F1 |
| 9 | Analisis | Pembahasan dan batasan |
| 10 | Tulis laporan | Laporan akhir |

---

## Tahap 1: Rumuskan Masalah dan Batas Penelitian

- [ ] Tulis pertanyaan penelitian (lihat di atas).
- [ ] Definisikan "satu petak": satu hamparan air atau kristal yang dikelilingi pematang.
- [ ] Tulis aturan untuk kasus sulit:
  - petak terbelah pematang kecil
  - petak sebagian di tepi tile
  - petak tertutup vegetasi
- [ ] Pakai aturan yang sama untuk hitungan manual dan evaluasi.
- [ ] Tetapkan lokasi: Desa Lembung dan satu desa di Pademawu.

## Tahap 2: Kumpulkan Data

- [ ] Pasang Google Earth Pro (desktop).
- [ ] Cari "Desa Lembung, Galis, Pamekasan" dan satu desa di Pademawu, lalu verifikasi bahwa blok petak teratur terlihat.
- [ ] Ambil citra: 2 lokasi, 2 sampai 3 tanggal, top view, utara di atas (tombol `U` dan `N`).
- [ ] Sembunyikan polygon, label, dan ikon sebelum menyimpan.
- [ ] Simpan sebagai PNG (bukan JPEG), resolusi tertinggi yang tersedia.
- [ ] Ketinggian pandang sekitar 500 sampai 1.000 m, sama untuk semua pengambilan.
- [ ] Catat tanggal sebenarnya. Format seperti 3/6/2025 ambigu (3 Maret atau 6 Juni).
- [ ] Isi log CSV dengan kolom:
  - nama file
  - desa
  - lintang dan bujur
  - tanggal citra
  - ketinggian pandang
  - jenis alas yang terlihat (tanah atau geomembran)
  - penyedia citra yang tertera di layar
- [ ] Potong menjadi 30 sampai 50 tile 512 x 512 piksel, hindari area logo atau atribusi.
- [ ] Beri nama file dengan pola tetap, misalnya `lembung_20250306_01.png`.
- [ ] Sertakan beberapa tile berkabut atau berpantulan cahaya untuk menguji preprocessing.

## Tahap 3: Siapkan Ground Truth

- [ ] Hitung jumlah petak manual di setiap tile sesuai aturan tahap 1.
- [ ] Hitung dua kali di hari berbeda dan bandingkan hasilnya.
- [ ] Opsional: gambar kotak atau mask tiap petak di LabelMe untuk 10 sampai 15 tile (untuk precision dan recall).
- [ ] Bagi data:
  - **Tile tuning** (sekitar sepertiga): untuk mengatur parameter.
  - **Tile uji** (sisanya): untuk hasil akhir.
- [ ] Jangan menyetel parameter pada tile uji.

## Tahap 4: Bangun Alur Preprocessing (Inti Penelitian)

Teknik yang diuji:

| Kelompok | Teknik |
|---|---|
| Penghilangan noise | Median, Gaussian, Bilateral |
| Peningkatan kontras | Histogram equalization, CLAHE |
| Sharpening | Unsharp masking, Laplacian |

Alur yang dibandingkan:

| Alur | Isi |
|---|---|
| A | Tanpa preprocessing (baseline) |
| B | Median |
| C | Median + CLAHE |
| D | Median + CLAHE + Unsharp masking |

## Tahap 5: Eksperimen Kualitas Citra (Khusus Noise)

PSNR dan SSIM butuh gambar acuan yang bersih. Citra asli tidak punya versi bersih, jadi dibuat eksperimen terkontrol.

- [ ] Pilih tile paling bersih sebagai acuan.
- [ ] Tambahkan noise buatan ke salinannya:
  - Gaussian (misalnya simpangan baku 15)
  - Salt-and-pepper (misalnya 2% piksel)
- [ ] Terapkan filter noise (median, Gaussian, bilateral).
- [ ] Hitung PSNR dan SSIM terhadap tile acuan.
- [ ] Hitung juga nilai untuk citra berisik tanpa filter sebagai pembanding dasar.
- [ ] Ulangi pada semua tile bersih dan ambil rata-ratanya.

Catatan:

- PSNR dan SSIM hanya dipakai untuk memilih filter noise.
- CLAHE dan sharpening sengaja mengubah kontras dan ketajaman, jadi tidak dinilai dengan kedua metrik ini.
- Tile acuan tetap membawa noise bawaan citra, jadi hasilnya perbandingan relatif antar filter.

Contoh kode:

```python
import cv2, numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

np.random.seed(0)
clean = cv2.imread("tile.png")
noisy = np.clip(clean + np.random.normal(0, 15, clean.shape), 0, 255).astype(np.uint8)
denoised = cv2.medianBlur(noisy, 5)

print("berisik :", psnr(clean, noisy), ssim(clean, noisy, channel_axis=2))
print("median  :", psnr(clean, denoised), ssim(clean, denoised, channel_axis=2))
```

## Tahap 6: Bangun Metode Penghitungan

Satu metode yang sama dipakai untuk semua alur, supaya perbedaan hasil berasal dari preprocessing.

1. Ubah ke grayscale atau pilih satu kanal yang paling jelas memisahkan pematang dari air.
2. Deteksi batas pematang: Canny atau thresholding.
3. Operasi morfologi:
   - closing untuk menutup celah pada pematang
   - opening untuk membuang bintik kecil
4. Balik hasil sehingga petak menjadi objek, lalu jalankan connected components.
5. Saring objek berdasarkan luas minimum dan maksimum.
6. Jumlah objek yang lolos adalah jumlah petak.
7. Jika banyak petak bersentuhan, tambahkan distance transform dan watershed.

## Tahap 7: Jalankan Eksperimen Utama

- [ ] Setel parameter (batas Canny, ukuran kernel morfologi, luas minimum) pada tile tuning dengan alur A saja.
- [ ] Kunci parameter itu untuk semua alur.
- [ ] Jalankan alur A sampai D pada tile uji.
- [ ] Simpan jumlah hitungan tiap alur per tile ke tabel.

## Tahap 8: Evaluasi

| Metrik | Fungsi |
|---|---|
| MAE | Rata-rata selisih absolut jumlah petak terhadap hitungan manual |
| MAPE | Persen kesalahan hitungan |
| Precision, Recall, F1 (opsional) | Pencocokan objek terdeteksi ke kotak manual dengan ambang IoU |

- [ ] Ringkas hasil per alur, per lokasi, dan per tanggal.

## Tahap 9: Analisis

- [ ] Alur mana yang paling kecil kesalahannya, dan apakah selisihnya konsisten antar lokasi dan tanggal.
- [ ] Kasus gagal:
  - petak sempit
  - atap permukiman
  - mangrove
  - bayangan
  - bintik pada air (penyebabnya belum dipastikan)
  - perbedaan alas tanah dan geomembran
- [ ] Batasan:
  - hanya dua lokasi di Pamekasan
  - citra dari satu penyedia
  - noise buatan belum tentu sama dengan noise nyata
  - definisi petak bersifat subjektif

## Tahap 10: Tulis Laporan

Susunan: latar belakang, tinjauan pustaka, metode, hasil, pembahasan, kesimpulan.

**Referensi awal** (baca paper lengkapnya sebelum dikutip):

- Purnama, Cahyawati, Hutapea (2018). *Salt Pond Analysis Using ALOS PALSAR Case Study Sampang, Madura-Indonesia.* Prosiding MSAT 2017. https://karya.brin.go.id/id/eprint/11539/
- Studi Landsat 8 untuk petak kristalisasi dan estimasi produksi garam (ACRS 2025, Filipina). https://acrs-aars.org/proceeding/ACRS2025/fp_abs-323.pdf
- Pemantauan Danau Garam Maharlu dengan citra ASTER. *Journal of Environmental Studies.* https://jes.ut.ac.ir/article_52212.html?lang=en
- Dalton dkk. (2005). *Hyperspectral studies of hypersaline ecosystems.* SPIE 5977. https://doi.org/10.1117/12.627438 (data hiperspektral, hanya sebagai landasan teori)

**Klaim yang masih perlu sumber tambahan:**

- Pemantauan tambak masih bergantung pada survei lapangan.
- Belum ada kajian pembanding preprocessing untuk citra tambak garam di Indonesia.
- Penyebab bintik putih pada permukaan petak.

---

## Keluaran Akhir

- [ ] Dataset tile, log CSV, dan hitungan manual
- [ ] Kode preprocessing dan penghitungan
- [ ] Tabel PSNR dan SSIM untuk filter noise
- [ ] Tabel MAE dan MAPE untuk alur A sampai D
- [ ] Contoh visual sebelum dan sesudah tiap alur, termasuk satu atau dua kasus gagal
