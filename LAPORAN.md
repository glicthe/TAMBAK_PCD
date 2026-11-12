# LAPORAN PENELITIAN

# Pengaruh Preprocessing (Penghilangan Noise, Peningkatan Kontras, dan Sharpening) terhadap Deteksi dan Penghitungan Petak Tambak Garam pada Citra Satelit (Studi Kasus: Madura)

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang

Madura merupakan salah satu pulau penghasil garam terbesar di Indonesia. Kabupaten Pamekasan, khususnya Kecamatan Galis dan Kecamatan Pademawu, memiliki lahan tambak garam yang luas dan menjadi sumber penghidupan masyarakat pesisir. Pemantauan kondisi tambak garam, termasuk penghitungan jumlah petak, hingga saat ini masih banyak bergantung pada survei lapangan yang membutuhkan waktu dan biaya besar.

Pemanfaatan citra satelit beresolusi tinggi membuka peluang untuk memantau tambak garam secara efisien. Beberapa penelitian terdahulu telah memanfaatkan citra penginderaan jauh untuk menganalisis tambak garam di Madura. Purnama dkk. (2018) menggunakan citra ALOS PALSAR untuk menganalisis tambak garam di Sampang. Mu'tamar dkk. (2021) menggunakan Landsat 8 untuk mengestimasi luas tambak di Sampang dengan akurasi 67,5% dan recall 60,6%. Efendy dkk. (2014) mengkaji potensi lahan tambak di Pamekasan, sedangkan Zainab dkk. (2018) memetakan salinitas menggunakan citra MODIS di perairan Sampang.

Namun, citra satelit yang digunakan untuk deteksi petak tambak garam umumnya mengandung noise dan memiliki variasi kontras yang besar, terutama pada citra yang diambil pada kondisi cuaca berbeda. Preprocessing citra berupa penghilangan noise, peningkatan kontras, dan sharpening merupakan langkah yang berpotensi meningkatkan akurasi deteksi. Meskipun demikian, belum ada kajian yang secara khusus membandingkan pengaruh berbagai alur preprocessing terhadap akurasi penghitungan petak tambak garam pada citra satelit di Indonesia.

### 1.2 Rumusan Masalah

Alur preprocessing mana yang paling meningkatkan akurasi penghitungan petak tambak garam pada citra satelit?

### 1.3 Tujuan Penelitian

Membandingkan pengaruh enam alur preprocessing (tanpa preprocessing, filter saja, filter + CLAHE, filter + CLAHE + unsharp masking, filter + histogram equalization, dan filter + CLAHE + Laplacian sharpening) terhadap akurasi penghitungan petak tambak garam, diukur dengan Mean Absolute Error (MAE) dan Mean Absolute Percentage Error (MAPE).

### 1.4 Batasan Penelitian

1. Penelitian ini berfokus pada preprocessing. Metode penghitungan petak hanya digunakan sebagai alat ukur dan tidak dikembangkan lebih lanjut.
2. Lokasi penelitian terbatas pada dua kecamatan di Kabupaten Pamekasan: Galis dan Pademawu.
3. Citra berasal dari satu penyedia (Google Earth Pro).
4. Dataset terdiri dari 26 tile berukuran 512x512 piksel.
5. Ketinggian pandang berbeda antar lokasi (sekitar 800 m untuk Pademawu dan sekitar 2600 m untuk Galis), sehingga skala petak sangat berbeda.
6. Definisi "petak" bersifat subjektif dan hitungan manual berasal dari satu orang.

---

## BAB II: TINJAUAN PUSTAKA

### 2.1 Tambak Garam

Tambak garam adalah lahan buatan di daerah pesisir yang digunakan untuk memproduksi garam melalui proses penguapan air laut. Secara fisik, tambak garam terdiri dari petak-petak berukuran teratur yang dibatasi oleh pematang (tanggul kecil). Setiap petak berfungsi sebagai wadah penguapan air laut, di mana air laut dialirkan dan dibiarkan menguap hingga kristal garam terbentuk.

### 2.2 Penginderaan Jauh untuk Tambak Garam

Purnama dkk. (2018) menggunakan citra ALOS PALSAR (radar) untuk menganalisis tambak garam di Sampang, Madura. Pendekatan radar memiliki keunggulan tidak bergantung pada kondisi cuaca, namun resolusi spasialnya terbatas untuk mendeteksi petak individual.

Mu'tamar dkk. (2021) menggunakan citra Landsat 8 untuk mengestimasi luas tambak kristalisasi dan memprediksi produksi garam di Sampang. Penelitian tersebut mencapai akurasi peta 67,5% dan recall 60,6%, menunjukkan bahwa pendekatan berbasis citra multispektral masih memiliki keterbatasan dalam akurasi.

Efendy dkk. (2014) mengkaji potensi lahan tambak garam di Pamekasan, menyediakan konteks wilayah untuk penelitian ini. Zainab dkk. (2018) menggunakan citra MODIS untuk memetakan salinitas perairan di Sampang, yang relevan dengan kondisi lingkungan tambak garam.

### 2.3 Preprocessing Citra Digital

#### 2.3.1 Penghilangan Noise (Denoising)

**Filter Median** mengganti nilai setiap piksel dengan median dari piksel-piksel dalam jendela bertetangga. Filter ini efektif menghilangkan noise salt-and-pepper tanpa mengaburkan tepi secara berlebihan (Gonzalez & Woods, 2018).

**Filter Gaussian** menerapkan konvolusi dengan kernel Gaussian, menghasilkan penghalusan yang proporsional terhadap jarak dari pusat kernel. Filter ini efektif untuk noise Gaussian tetapi cenderung mengaburkan tepi.

**Filter Bilateral** mempertimbangkan kedekatan spasial dan kesamaan intensitas secara bersamaan, sehingga mampu menghaluskan area homogen tanpa mengaburkan tepi yang kuat. Namun, pada tepi yang lemah seperti pematang tipis, filter bilateral dengan parameter sigmaColor yang besar dapat menghapus tepi tersebut.

#### 2.3.2 Peningkatan Kontras

**Histogram Equalization** meratakan histogram intensitas sehingga seluruh rentang intensitas digunakan secara merata. Teknik ini meningkatkan kontras secara global tetapi dapat memangkas detail pada area yang sangat terang atau sangat gelap.

**CLAHE (Contrast Limited Adaptive Histogram Equalization)** membagi citra menjadi blok-blok kecil (tile) dan menerapkan histogram equalization secara lokal pada setiap blok, dengan pembatasan clip limit untuk mencegah amplifikasi noise. Metode ini lebih adaptif dibandingkan histogram equalization global.

#### 2.3.3 Sharpening

**Unsharp Masking** meningkatkan ketajaman dengan menambahkan versi high-pass dari citra ke citra asli. Secara matematis, hasil = citra + amount * (citra - blur(citra)).

**Laplacian Sharpening** menggunakan operator Laplacian (turunan kedua) untuk mendeteksi perubahan intensitas cepat, lalu menguranginya dari citra asli untuk mempertajam tepi. Secara matematis, hasil = citra - amount * Laplacian(citra).

### 2.4 Deteksi Tepi

**Operator Canny** mendeteksi tepi menggunakan gradien intensitas dengan dua ambang batas (low dan high) melalui mekanisme hysteresis. Tepi dengan gradien di atas ambang tinggi langsung diterima, sedangkan tepi dengan gradien antara ambang rendah dan tinggi diterima hanya jika terhubung dengan tepi kuat.

**Operator Kirsch** menggunakan delapan kernel konvolusi 3x3, masing-masing merepresentasikan satu arah (0, 45, 90, ..., 315 derajat). Magnitude tepi diambil sebagai respons maksimum dari kedelapan kernel. Operator ini lebih sensitif terhadap tepi pada berbagai orientasi dibandingkan operator berbasis gradien tunggal.

### 2.5 Metrik Evaluasi

**Mean Absolute Error (MAE)** mengukur rata-rata selisih absolut antara jumlah petak yang diprediksi dan jumlah sebenarnya (ground truth).

$$MAE = \frac{1}{n} \sum_{i=1}^{n} |pred_i - truth_i|$$

**Mean Absolute Percentage Error (MAPE)** mengukur persentase rata-rata kesalahan relatif terhadap nilai sebenarnya.

$$MAPE = \frac{1}{n} \sum_{i=1}^{n} \frac{|pred_i - truth_i|}{truth_i} \times 100\%$$

**PSNR (Peak Signal-to-Noise Ratio)** mengukur kualitas citra hasil filtering dibandingkan citra acuan. Nilai PSNR yang lebih tinggi menunjukkan kualitas yang lebih baik.

**SSIM (Structural Similarity Index)** mengukur kesamaan struktural antara dua citra, mempertimbangkan luminansi, kontras, dan struktur. Nilai SSIM berkisar 0 sampai 1, di mana 1 berarti identik.

---

## BAB III: METODE PENELITIAN

### 3.1 Data Penelitian

Data yang digunakan berupa citra dari Google Earth Pro pada dua lokasi di Kabupaten Pamekasan, Madura:

| Parameter | Pademawu | Galis |
|---|---|---|
| Koordinat | 7°12'41.57"S 113°33'10.96"E | 7°11'52.12"S 113°33'01.75"E |
| Ketinggian pandang | ~800 m | ~2600 m |
| Jumlah tile | 12 | 14 |

Tanggal citra yang digunakan:
- 3 Mei 2020
- 22 Agustus 2022
- 8 Mei 2023

Total 26 tile berukuran 512x512 piksel dipotong dari citra satelit. Setiap tile diberi nama dengan format `lokasi_tanggal_nomor.png`.

### 3.2 Definisi Petak

Satu petak didefinisikan sebagai satu hamparan tertutup (berisi air, kristal garam, atau kosong) yang seluruh sisinya dibatasi pematang yang terlihat jelas di citra.

Aturan untuk kasus sulit:
- Petak terbelah pematang kecil: dihitung dua jika sekat membentuk batas tertutup yang jelas. Sekat samar atau putus tidak memisahkan petak.
- Petak sebagian di tepi tile: dihitung jika setengah atau lebih luas petak terlihat.
- Petak tertutup vegetasi: dihitung jika lebih dari setengah masih terlihat dan batas pematang jelas.
- Petak kering atau kosong: tetap dihitung selama berpematang dan merupakan bagian dari blok tambak.

### 3.3 Ground Truth dan Pembagian Data

Jumlah petak pada setiap tile dihitung secara manual sesuai definisi di atas. Data dibagi menjadi:

| Set | Pademawu | Galis | Total |
|---|---|---|---|
| Tuning | 4 tile | 5 tile | 9 tile |
| Uji | 8 tile | 9 tile | 17 tile |

Setiap lokasi dan tanggal terwakili di kedua set. Tile tuning digunakan untuk menyetel parameter penghitung, sedangkan tile uji digunakan untuk evaluasi akhir.

**Tile uji Pademawu** (8 tile, ground truth):

| Tile | Tanggal | Jumlah Petak |
|---|---|---|
| pademawu_03052020_02 | 3 Mei 2020 | 111 |
| pademawu_03052020_03 | 3 Mei 2020 | 110 |
| pademawu_03052020_04 | 3 Mei 2020 | 85 |
| pademawu_08052023_01 | 8 Mei 2023 | 135 |
| pademawu_08052023_03 | 8 Mei 2023 | 119 |
| pademawu_22082022_01 | 22 Ags 2022 | 123 |
| pademawu_22082022_02 | 22 Ags 2022 | 119 |
| pademawu_22082022_04 | 22 Ags 2022 | 89 |

**Tile uji Galis** (9 tile, ground truth):

| Tile | Tanggal | Jumlah Petak |
|---|---|---|
| galis_03052020_01 | 3 Mei 2020 | 197 |
| galis_03052020_04 | 3 Mei 2020 | 188 |
| galis_03052020_05 | 3 Mei 2020 | 295 |
| galis_03052020_06 | 3 Mei 2020 | 293 |
| galis_08052023_02 | 8 Mei 2023 | 501 |
| galis_08052023_03 | 8 Mei 2023 | 435 |
| galis_08052023_04 | 8 Mei 2023 | 490 |
| galis_22082022_01 | 22 Ags 2022 | 321 |
| galis_22082022_02 | 22 Ags 2022 | 488 |

### 3.4 Alur Preprocessing

Enam alur preprocessing yang dibandingkan:

| Alur | Deskripsi |
|---|---|
| A | Tanpa preprocessing (baseline) |
| B | Filter (denoising saja) |
| C | Filter + CLAHE |
| D | Filter + CLAHE + Unsharp Masking |
| E | Filter + Histogram Equalization |
| F | Filter + CLAHE + Laplacian Sharpening |

Setiap alur dijalankan dengan dua jenis filter denoising:
- **Median** (kernel 5x5)
- **Bilateral** (d=9, sigmaColor=75, sigmaSpace=75)

Alur A tidak menggunakan filter apapun, sehingga hasilnya identik di kedua set.

Parameter preprocessing yang digunakan (terkunci sebelum penghitungan):

| Parameter | Nilai |
|---|---|
| Median kernel | 5 |
| Gaussian kernel | 5 |
| Gaussian sigma | 0 (diturunkan dari ukuran kernel) |
| Bilateral d | 9 |
| Bilateral sigmaColor | 75 |
| Bilateral sigmaSpace | 75 |
| CLAHE clipLimit | 2.0 |
| CLAHE tileGridSize | 8x8 |
| Unsharp sigma | 1.0 |
| Unsharp amount | 1.0 |
| Laplacian amount | 0.5 |

Peningkatan kontras (CLAHE dan histogram equalization) diterapkan hanya pada kanal L (lightness) di ruang warna CIELAB, agar warna tidak berubah.

### 3.5 Metode Penghitungan Petak

Penghitungan petak dilakukan dengan langkah-langkah berikut:

1. **Konversi ke grayscale.**
2. **Deteksi tepi pematang** menggunakan operator Kirsch:
   - Hitung magnitude tepi dari 8 kernel arah.
   - Normalisasi per tile menggunakan persentil ke-99,5.
   - Tentukan ambang batas dengan metode Otsu, lalu kalikan dengan faktor `thr_scale`.
   - Hapus komponen kecil (speck) jika `speck_area` > 0.
   - Dilasi mask tepi jika `dilate_k` > 1.
3. **Inversi**: balik mask tepi sehingga petak menjadi objek putih.
4. **Opening** morfologi (kernel 3x3) untuk menghilangkan bintik kecil.
5. **Connected components** (konektivitas 4) untuk menghitung objek.
6. **Saring** berdasarkan luas: hanya objek dengan luas antara `min_area` dan `max_area` yang dihitung sebagai petak.

Parameter penghitung disetel hanya pada tile tuning dengan alur A, lalu dikunci untuk semua alur.

**Parameter penghitung Kirsch terkunci:**

| Parameter | Pademawu | Galis |
|---|---|---|
| thr_scale | 1.2 | 0.8 |
| speck_area | 0 | 0 |
| dilate_k | 3 | 3 |
| min_area | 20 | 20 |
| open_k | 3 | 3 |
| max_area | 100000 | 100000 |

### 3.6 Riwayat Penghitung Versi 1 (Canny)

Sebelum menggunakan Kirsch, deteksi tepi Canny digunakan terlebih dahulu (versi 1). Parameter Canny untuk Pademawu: low=30, high=100, close_k=7, min_area=200. Parameter Canny untuk Galis: low=80, high=100, close_k=3, min_area=50.

Canny gagal total pada tile 3 Mei 2020 yang berkontras rendah: hampir tidak ada tepi yang terdeteksi, sehingga hasil inversi menghasilkan satu wilayah besar yang melebihi max_area, dan prediksi menjadi 0. Setelah melihat kegagalan ini, penghitung diganti ke Kirsch yang lebih robust berkat threshold adaptif per tile.

Penggantian penghitung setelah melihat hasil uji berarti Pademawu bukan lagi uji murni untuk penghitung versi 2. Hasil kedua versi ditampilkan terpisah.

### 3.7 Eksperimen Kualitas Citra (Noise)

Untuk mengevaluasi kemampuan setiap filter dalam menghilangkan noise, dilakukan eksperimen terkontrol:

1. Pilih 6 tile terbersih sebagai citra acuan.
2. Tambahkan noise buatan:
   - Noise Gaussian (simpangan baku 15)
   - Noise salt-and-pepper (2% piksel)
3. Terapkan tiga filter (median, Gaussian, bilateral) pada citra berisik.
4. Hitung PSNR dan SSIM terhadap citra acuan.
5. Hitung juga nilai untuk citra berisik tanpa filter sebagai pembanding dasar (`none`).

PSNR dan SSIM hanya digunakan untuk mengevaluasi filter noise. CLAHE dan sharpening sengaja mengubah kontras dan ketajaman, sehingga tidak dinilai dengan kedua metrik ini.

### 3.8 Metrik Evaluasi

- **MAE** dan **MAPE** untuk mengukur akurasi penghitungan petak.
- **Bias** (pred - truth): bias negatif menunjukkan petak menyatu (undercounting), bias positif menunjukkan petak terpecah atau tepi palsu (overcounting).
- **PSNR** dan **SSIM** untuk mengukur kualitas denoising.

---

## BAB IV: HASIL

### 4.1 Hasil Eksperimen Kualitas Citra (PSNR dan SSIM)

**Tabel 1. Rata-rata PSNR dan SSIM filter denoising pada noise buatan (6 tile acuan)**

| Noise | Filter | PSNR | SSIM |
|---|---|---|---|
| Gaussian | Tanpa filter | 24.663 | 0.6756 |
| Gaussian | Median | 26.347 | 0.7493 |
| Gaussian | Gaussian | 28.802 | 0.8540 |
| Gaussian | Bilateral | **30.221** | **0.8726** |
| Salt-and-pepper | Tanpa filter | 22.112 | 0.7264 |
| Salt-and-pepper | Median | 27.365 | 0.8057 |
| Salt-and-pepper | Gaussian | **27.914** | **0.8283** |
| Salt-and-pepper | Bilateral | 21.895 | 0.6604 |

Untuk noise Gaussian, filter bilateral menghasilkan PSNR dan SSIM tertinggi (30.221 dB dan 0.8726), diikuti filter Gaussian (28.802 dB dan 0.8540), lalu median (26.347 dB dan 0.7493). Ketiga filter memperbaiki citra dibandingkan tanpa filter.

Untuk noise salt-and-pepper, filter Gaussian menghasilkan PSNR dan SSIM tertinggi (27.914 dB dan 0.8283), diikuti median (27.365 dB dan 0.8057). Filter bilateral justru memperburuk citra (PSNR 21.895, lebih rendah dari tanpa filter 22.112; SSIM 0.6604, lebih rendah dari 0.7264).

### 4.2 Hasil Penghitungan Petak: Versi 1 (Canny, Arsip)

Hasil ini menggunakan penghitung Canny (versi 1) dengan filter median. Ditampilkan sebagai riwayat dan alasan penggantian penghitung.

**Tabel 2. Pademawu, Canny, Median (8 tile uji)**

| Alur | MAE | MAPE |
|---|---|---|
| A | 46.1 | 44.2% |
| B | 49.8 | 48.3% |
| C | 31.5 | 29.8% |
| D | 29.0 | 25.4% |

**Tabel 3. Galis, Canny, Median (9 tile uji)**

| Alur | MAE | MAPE |
|---|---|---|
| A | 155.2 | 55.8% |
| B | 229.3 | 70.9% |
| C | 137.7 | 52.2% |
| D | 191.6 | 64.7% |

Masalah utama: tile 3 Mei 2020 diprediksi 0 pada alur A dan B karena Canny gagal mendeteksi tepi pada citra berkontras rendah.

### 4.3 Hasil Penghitungan Petak: Versi 2 (Kirsch)

#### 4.3.1 Pademawu

**Tabel 4. Pademawu, Kirsch, Filter Median (8 tile uji)**

| Alur | n | MAE | MAPE | Bias |
|---|---|---|---|---|
| **A** | 8 | **16.88** | **16.62%** | +10.88 |
| B | 8 | 50.75 | 44.51% | -50.75 |
| C | 8 | 46.13 | 39.87% | -46.12 |
| D | 8 | 48.25 | 40.82% | -48.25 |
| E | 8 | 58.88 | 50.51% | -58.88 |
| F | 8 | 56.00 | 49.39% | -56.00 |

**Tabel 5. Pademawu, Kirsch, Filter Median, MAE per tanggal**

| Alur | 3 Mei 2020 (3 tile) | 22 Ags 2022 (3 tile) | 8 Mei 2023 (2 tile) |
|---|---|---|---|
| A | 14.33 (15.05%) | 27.00 (26.43%) | 5.50 (4.28%) |
| B | 38.67 (37.51%) | 52.67 (46.83%) | 66.00 (51.53%) |
| C | 34.00 (32.19%) | 44.33 (39.69%) | 67.00 (51.67%) |
| D | 30.00 (27.55%) | 42.33 (37.48%) | 84.50 (65.73%) |
| E | 30.67 (28.90%) | 63.33 (56.47%) | 94.50 (73.98%) |
| F | 60.67 (58.50%) | 38.67 (34.34%) | 75.00 (58.30%) |

**Tabel 6. Pademawu, Kirsch, Filter Bilateral (8 tile uji)**

| Alur | n | MAE | MAPE | Bias |
|---|---|---|---|---|
| **A** | 8 | **16.88** | **16.62%** | +10.88 |
| B | 8 | 71.38 | 63.54% | -71.38 |
| C | 8 | 72.00 | 63.90% | -72.00 |
| D | 8 | 63.25 | 55.17% | -63.25 |
| E | 8 | 79.13 | 69.64% | -79.12 |
| F | 8 | 133.00 | 123.15% | +59.75 |

**Tabel 7. Pademawu, Kirsch, Filter Bilateral, MAE per tanggal**

| Alur | 3 Mei 2020 (3 tile) | 22 Ags 2022 (3 tile) | 8 Mei 2023 (2 tile) |
|---|---|---|---|
| A | 14.33 (15.05%) | 27.00 (26.43%) | 5.50 (4.28%) |
| B | 64.00 (61.45%) | 78.00 (70.12%) | 72.50 (56.79%) |
| C | 55.67 (54.31%) | 81.67 (73.27%) | 82.00 (64.22%) |
| D | 26.33 (26.42%) | 82.00 (73.45%) | 90.50 (70.88%) |
| E | 52.33 (51.18%) | 89.00 (79.75%) | 104.50 (82.19%) |
| F | 257.00 (243.52%) | 78.67 (70.16%) | 28.50 (22.06%) |

#### 4.3.2 Galis

**Tabel 8. Galis, Kirsch, Filter Median (9 tile uji)**

| Alur | n | MAE | MAPE | Bias |
|---|---|---|---|---|
| **A** | 9 | **29.67** | **7.91%** | -19.00 |
| B | 9 | 193.00 | 53.18% | -193.00 |
| C | 9 | 140.33 | 37.83% | -140.33 |
| D | 9 | 133.89 | 36.10% | -133.00 |
| E | 9 | 155.11 | 42.04% | -151.33 |
| F | 9 | 84.22 | 24.44% | -75.78 |

**Tabel 9. Galis, Kirsch, Filter Median, MAE per tanggal**

| Alur | 3 Mei 2020 (4 tile) | 22 Ags 2022 (2 tile) | 8 Mei 2023 (3 tile) |
|---|---|---|---|
| A | 14.75 (6.58%) | 65.00 (13.80%) | 26.00 (5.74%) |
| B | 135.00 (53.54%) | 222.50 (52.89%) | 250.67 (52.89%) |
| C | 100.25 (37.80%) | 173.50 (40.35%) | 171.67 (36.19%) |
| D | 99.00 (36.67%) | 167.50 (39.12%) | 158.00 (33.34%) |
| E | 94.50 (38.63%) | 172.50 (41.11%) | 224.33 (47.20%) |
| F | 95.50 (34.73%) | 66.00 (14.64%) | 81.33 (17.26%) |

**Tabel 10. Galis, Kirsch, Filter Bilateral (9 tile uji)**

| Alur | n | MAE | MAPE | Bias |
|---|---|---|---|---|
| **A** | 9 | **29.67** | **7.91%** | -19.00 |
| B | 9 | 185.11 | 50.26% | -185.11 |
| C | 9 | 130.33 | 34.70% | -124.33 |
| D | 9 | 163.67 | 49.32% | -36.11 |
| E | 9 | 144.78 | 39.38% | -141.00 |
| F | 9 | 79.33 | 26.56% | -31.33 |

**Tabel 11. Galis, Kirsch, Filter Bilateral, MAE per tanggal**

| Alur | 3 Mei 2020 (4 tile) | 22 Ags 2022 (2 tile) | 8 Mei 2023 (3 tile) |
|---|---|---|---|
| A | 14.75 (6.58%) | 65.00 (13.80%) | 26.00 (5.74%) |
| B | 108.50 (43.84%) | 284.50 (68.48%) | 221.00 (46.67%) |
| C | 67.25 (27.30%) | 228.00 (54.18%) | 149.33 (31.58%) |
| D | 143.50 (60.52%) | 223.00 (53.05%) | 151.00 (31.92%) |
| E | 77.50 (32.63%) | 229.00 (55.19%) | 178.33 (37.85%) |
| F | 82.25 (38.10%) | 116.00 (26.70%) | 51.00 (11.09%) |

### 4.4 Ringkasan Perbandingan Antar Alur

**Tabel 12. Ringkasan MAE (MAPE) semua kelompok**

| Alur | Pademawu Median | Pademawu Bilateral | Galis Median | Galis Bilateral |
|---|---|---|---|---|
| A | **16.88 (16.62%)** | **16.88 (16.62%)** | **29.67 (7.91%)** | **29.67 (7.91%)** |
| B | 50.75 (44.51%) | 71.38 (63.54%) | 193.00 (53.18%) | 185.11 (50.26%) |
| C | 46.13 (39.87%) | 72.00 (63.90%) | 140.33 (37.83%) | 130.33 (34.70%) |
| D | 48.25 (40.82%) | 63.25 (55.17%) | 133.89 (36.10%) | 163.67 (49.32%) |
| E | 58.88 (50.51%) | 79.13 (69.64%) | 155.11 (42.04%) | 144.78 (39.38%) |
| F | 56.00 (49.39%) | 133.00 (123.15%) | 84.22 (24.44%) | 79.33 (26.56%) |

### 4.5 Hasil Per Tile (Detail)

#### Pademawu, Kirsch, Median

| Tile | Truth | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| pademawu_03052020_02 | 111 | 101 | 62 | 59 | 50 | 63 | 31 |
| pademawu_03052020_03 | 110 | 100 | 71 | 76 | 86 | 79 | 48 |
| pademawu_03052020_04 | 85 | 108 | 57 | 69 | 80 | 72 | 45 |
| pademawu_08052023_01 | 135 | 142 | 56 | 42 | 29 | 26 | 40 |
| pademawu_08052023_03 | 119 | 115 | 66 | 78 | 56 | 39 | 64 |
| pademawu_22082022_01 | 123 | 138 | 53 | 69 | 63 | 45 | 67 |
| pademawu_22082022_02 | 119 | 144 | 65 | 71 | 78 | 49 | 84 |
| pademawu_22082022_04 | 89 | 130 | 55 | 58 | 63 | 47 | 64 |

#### Galis, Kirsch, Median

| Tile | Truth | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| galis_03052020_01 | 197 | 222 | 143 | 183 | 201 | 214 | 214 |
| galis_03052020_04 | 188 | 199 | 76 | 123 | 129 | 67 | 156 |
| galis_03052020_05 | 295 | 275 | 101 | 125 | 129 | 132 | 127 |
| galis_03052020_06 | 293 | 296 | 113 | 141 | 126 | 216 | 128 |
| galis_08052023_02 | 501 | 491 | 256 | 336 | 355 | 272 | 435 |
| galis_08052023_03 | 435 | 383 | 191 | 272 | 282 | 231 | 347 |
| galis_08052023_04 | 490 | 474 | 227 | 303 | 315 | 250 | 400 |
| galis_22082022_01 | 321 | 330 | 184 | 231 | 231 | 213 | 342 |
| galis_22082022_02 | 488 | 367 | 180 | 231 | 243 | 251 | 377 |

---

## BAB V: PEMBAHASAN

### 5.1 Alur A (Tanpa Preprocessing) Paling Akurat

Temuan utama penelitian ini: **alur A (tanpa preprocessing) menghasilkan akurasi penghitungan petak terbaik di kedua lokasi**. Di Pademawu, MAE alur A adalah 16.88 (MAPE 16.62%), sedangkan alur preprocessing terbaik (alur C, median) memiliki MAE 46.13 (MAPE 39.87%), hampir tiga kali lipat lebih buruk. Di Galis, perbedaannya lebih besar: MAE alur A hanya 29.67 (MAPE 7.91%), sedangkan alur preprocessing terbaik setelah A (alur F, bilateral) memiliki MAE 79.33 (MAPE 26.56%).

Keunggulan alur A konsisten di seluruh tanggal dan di kedua jenis filter. Tidak ada alur preprocessing yang menandingi alur A di kelompok manapun.

### 5.2 Mengapa Preprocessing Memperburuk Akurasi

Semua alur preprocessing (B sampai F) pada kedua lokasi menghasilkan bias negatif yang besar (kecuali alur F bilateral Pademawu), yang berarti penghitung mendeteksi lebih sedikit petak dari seharusnya. Penyebab utamanya adalah **pematang tipis yang hilang setelah filtering**, menyebabkan petak-petak bertetangga menyatu menjadi satu objek.

**Filter median** (kernel 5x5) sudah cukup untuk menghilangkan pematang tipis, yang lebarnya sering hanya 1-3 piksel pada citra resolusi ini. Efeknya terlihat jelas di Pademawu: alur B (median saja) memiliki bias -50.75, artinya rata-rata 50 petak "hilang" per tile karena penyatuan.

**Filter bilateral** (sigmaColor=75) lebih parah lagi. Meskipun bilateral seharusnya mempertahankan tepi, parameter sigmaColor=75 membuat filter menganggap pematang tipis (yang perbedaan intensitasnya kecil dengan isi petak) sebagai bagian dari area homogen dan menghaluskannya. Di Pademawu bilateral, alur B memiliki bias -71.38, lebih buruk dari median (-50.75).

**CLAHE** (alur C) dan **histogram equalization** (alur E) tidak memperbaiki masalah pematang yang sudah hilang oleh filter. Bahkan histogram equalization cenderung memperburuk: pada Pademawu median, alur E (MAE 58.88) lebih buruk dari alur B (MAE 50.75). Histogram equalization memangkas area terang dan gelap serta menurunkan kontras pematang pada area yang sudah terang.

**Unsharp masking** (alur D) seharusnya mempertajam tepi, tetapi tidak mampu memulihkan pematang yang sudah hilang oleh filter. Hasilnya tidak berbeda jauh dari alur C.

### 5.3 Kasus Khusus: Alur F

Alur F (CLAHE + Laplacian sharpening) menunjukkan perilaku yang berbeda dari alur lainnya:

- Di **Galis median**, alur F memiliki MAE 84.22 (MAPE 24.44%), yang merupakan kedua terbaik setelah A. Laplacian sharpening tampak mampu memunculkan kembali sebagian pematang yang dihaluskan oleh median.

- Di **Galis bilateral**, alur F juga kedua terbaik (MAE 79.33, MAPE 26.56%).

- Di **Pademawu bilateral**, alur F justru paling buruk (MAE 133.00, MAPE 123.15%) dengan bias sangat positif (+59.75). Ini disebabkan oleh halo putih dan tepi palsu yang dihasilkan Laplacian pada tile 2020 Pademawu, di mana prediksi mencapai 506 dan 363 pada tile yang sebenarnya hanya berisi 111 dan 110 petak.

Inkonsistensi ini menunjukkan bahwa alur F tidak robust: performanya sangat bergantung pada karakteristik citra.

### 5.4 Perbedaan Antar Lokasi

MAE absolut Galis jauh lebih besar dari Pademawu karena jumlah petak per tile Galis lebih banyak (rata-rata 356 vs 112). Namun dalam MAPE, pola yang sama terlihat: alur A terbaik di kedua lokasi.

Di Galis, perbedaan antara alur A dan alur preprocessing lebih besar (MAPE 7.91% vs 24.44-53.18%) dibandingkan di Pademawu (16.62% vs 39.87-69.64%). Ini menunjukkan bahwa pada citra dengan petak kecil (Galis, ketinggian pandang 2600 m), pematang yang lebih kecil lebih rentan hilang oleh filtering.

### 5.5 Pengaruh Tanggal Citra

Tile 3 Mei 2020 di kedua lokasi lebih berkabut dan berkontras rendah. Pada versi 1 (Canny), tile ini gagal total (prediksi 0). Pada versi 2 (Kirsch), tile 2020 masih bisa dideteksi: MAE alur A untuk Pademawu 2020 adalah 14.33, hanya sedikit lebih buruk dari keseluruhan.

Alur F bilateral Pademawu menunjukkan kegagalan parah pada tile 2020 (MAE 257.00 dari 3 tile), di mana kombinasi Laplacian dan kontras rendah menghasilkan tepi palsu masif.

### 5.6 Analisis Kualitas Filter (PSNR dan SSIM)

Hasil eksperimen noise buatan menunjukkan bahwa:

1. Untuk **noise Gaussian**, bilateral paling baik (PSNR 30.221, SSIM 0.8726), diikuti Gaussian, lalu median.
2. Untuk **noise salt-and-pepper**, Gaussian paling baik (PSNR 27.914, SSIM 0.8283), diikuti median. Bilateral justru memperburuk (PSNR 21.895, lebih rendah dari tanpa filter).

Paradoks muncul: filter bilateral terbaik untuk noise Gaussian dalam PSNR/SSIM, tetapi paling buruk dalam akurasi penghitungan petak. Ini karena PSNR dan SSIM mengukur kualitas keseluruhan citra, sedangkan penghitungan petak bergantung pada struktur pematang tipis yang justru dikorbankan oleh bilateral.

### 5.7 Mengapa Parameter Penghitung Menguntungkan Alur A

Parameter penghitung Kirsch disetel pada tile tuning menggunakan alur A (tanpa preprocessing). Artinya, parameter tersebut dioptimalkan untuk mengenali tepi pada citra asli. Ketika parameter yang sama diterapkan pada citra yang sudah di-filter (alur B-F), hasilnya tidak optimal karena karakteristik tepi sudah berubah.

Ini adalah keputusan desain yang disengaja sesuai prosedur penelitian: parameter penghitung hanya boleh disetel sekali pada alur A. Jika parameter disetel ulang per alur, hasilnya mungkin berbeda, tetapi itu akan mengukur seberapa baik penghitung bisa disetel, bukan pengaruh murni preprocessing.

### 5.8 Kasus Gagal

1. **Pematang tipis hilang setelah filtering.** Terlihat jelas pada panel debug tile pademawu_22082022_03: pematang horizontal tipis yang tampak di alur A tidak terlihat setelah bilateral.

2. **Histogram equalization menurunkan kontras pematang di area terang.** Perataan histogram global memangkas rentang intensitas tinggi di mana pematang membentuk kontras tipis terhadap air.

3. **Halo dan tepi palsu pada alur F.** Laplacian sharpening dengan amount 0.5 menghasilkan cincin putih di sekitar tepi yang kuat, yang terdeteksi sebagai petak palsu pada tile berkontras rendah.

4. **Tile 2020 berkabut dan berkontras rendah.** Citra 3 Mei 2020 berkabut, mengurangi kontras pematang. Canny gagal total, Kirsch berhasil sebagian.

5. **Bangunan terdeteksi sebagai tepi.** Bangunan di pojok kanan bawah tile Pademawu 2022 menghasilkan tepi kuat yang terdeteksi sebagai petak.

6. **Area vegetasi dan sungai di Galis.** Elemen non-tambak ini menghasilkan tepi yang mengganggu penghitungan.

7. **Bintik di dalam petak.** Bintik putih pada permukaan air petak menyebabkan petak terpecah menjadi beberapa objek. Penyebab bintik ini belum dapat dipastikan.

8. **Perbedaan alas tanah dan geomembran.** Petak dengan alas berbeda memiliki kontras pematang yang berbeda, mempengaruhi deteksi tepi secara tidak seragam.

### 5.9 Saling Menutupi Kesalahan (Cancellation)

Di alur A Pademawu (median), bias +10.88 menunjukkan sedikit overcounting. Namun MAE 16.88 lebih besar dari bias, artinya ada tile yang overcounting dan tile yang undercounting. Dua jenis kesalahan (petak menyatu dan petak terpecah) bisa saling menutupi dalam rata-rata bias. Tanpa pencocokan spasial per petak (overlay), tidak bisa diketahui apakah petak yang benar memang terdeteksi dengan benar.

---

## BAB VI: KESIMPULAN

### 6.1 Kesimpulan

1. **Alur A (tanpa preprocessing) menghasilkan akurasi penghitungan petak terbaik** di kedua lokasi dan dengan kedua jenis filter. Di Pademawu, MAPE alur A adalah 16.62% dibandingkan 39.87% untuk alur preprocessing terbaik (C, median). Di Galis, MAPE alur A adalah 7.91% dibandingkan 24.44% untuk alur preprocessing terbaik (F, median).

2. **Semua alur preprocessing memperburuk akurasi penghitungan** karena filter denoising menghilangkan pematang tipis yang menjadi pembatas antar petak. Efek ini lebih parah pada filter bilateral dibandingkan median.

3. **Filter bilateral unggul dalam metrik kualitas citra** (PSNR dan SSIM terbaik untuk noise Gaussian), tetapi justru **paling merusak pematang tipis** dan menghasilkan akurasi penghitungan terburuk.

4. **Penghitung Kirsch lebih robust dibandingkan Canny** terhadap variasi kontras antar tanggal. Canny gagal total pada citra 2020 yang berkontras rendah, sedangkan Kirsch masih menghasilkan prediksi yang bisa diterima.

5. **Alur F (CLAHE + Laplacian)** menunjukkan potensi di Galis (MAPE 24.44%), tetapi tidak robust dan gagal parah di Pademawu bilateral (MAPE 123.15%) karena halo dan tepi palsu.

### 6.2 Batasan

1. Penghitung diganti dari Canny ke Kirsch setelah melihat hasil uji versi 1, sehingga Pademawu bukan uji murni untuk penghitung versi 2.
2. Parameter penghitung disetel hanya pada alur A, yang secara struktural menguntungkan A.
3. Ketinggian pandang berbeda antar lokasi (~800 m dan ~2600 m), sehingga skala petak sangat berbeda dan parameter penghitung disetel terpisah per lokasi.
4. Hanya 26 tile (8 tile uji Pademawu, 9 tile uji Galis). Dengan jumlah sampel kecil ini, selisih MAE yang kecil antar alur belum tentu signifikan secara statistik.
5. Parameter Kirsch Pademawu (thr_scale 1.2, speck_area 0, min_area 20) berada di tepi grid tuning, sehingga optimum mungkin di luar grid yang dicoba.
6. Galat jumlah bisa menutupi kesalahan segmentasi: petak yang menyatu dan petak yang terpecah saling meniadakan dalam hitungan.
7. Parameter filter menggunakan nilai bawaan tanpa penyetelan terpisah. Bilateral dengan sigmaColor 75 menghapus pematang tipis.
8. Citra dari satu penyedia (Google Earth Pro). Noise buatan di eksperimen kualitas belum tentu merepresentasikan noise nyata. Tile acuan masih membawa noise bawaannya sendiri.
9. Definisi petak bersifat subjektif. Hitungan manual berasal dari satu orang, dan hanya satu hitungan final yang tersimpan (target roadmap meminta dua hitungan di hari berbeda).
10. Hanya dua lokasi di satu kabupaten. Hasil belum bisa digeneralisasi ke wilayah tambak garam lain.

### 6.3 Saran

1. Gunakan parameter filter yang lebih kecil (kernel 3, sigmaColor lebih rendah) untuk mengurangi kehilangan pematang tipis, lalu ulangi perbandingan.
2. Lakukan penyetelan parameter filter secara terpisah, berdasarkan pemeriksaan visual mempertahankan pematang, bukan berdasarkan hasil penghitungan.
3. Perbanyak tile dan lokasi untuk hasil yang lebih general.
4. Gunakan citra dengan resolusi spasial yang diketahui (bukan Google Earth Pro) agar skala piksel-ke-meter konsisten.
5. Gunakan anotasi spasial (bounding box atau mask per petak) agar evaluasi bisa menggunakan precision, recall, dan F1 alih-alih hanya perbandingan jumlah.

---

## DAFTAR PUSTAKA

Efendy, M., dkk. (2014). Potensi lahan tambak garam di Kabupaten Pamekasan.

Gonzalez, R.C. & Woods, R.E. (2018). *Digital Image Processing* (4th ed.). Pearson.

Mu'tamar, M.F.F., dkk. (2021). Landsat 8 untuk estimasi luas tambak kristalisasi dan produksi garam di Sampang.

Purnama, S., Cahyawati, D., & Hutapea, Y.A. (2018). Salt Pond Analysis Using ALOS PALSAR Case Study Sampang, Madura-Indonesia. Prosiding MSAT 2017.

Zainab, S., dkk. (2018). Pemetaan salinitas menggunakan citra MODIS di perairan Sampang.
