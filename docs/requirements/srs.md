# Software Requirements Specification (SRS) - AutoPartSmart

**Versi:** 1.0  
**Tanggal:** 19 September 2026  
**Status:** Draf Ringkas  
**Standar Kualitas:** ISO/IEC 25010 (Functional Suitability, Performance Efficiency, Usability, Security, Reliability)  
**Platform & Stack:** Website — Frontend: React.js/Next.js, Backend: Python FastAPI/Flask, Database: PostgreSQL, AI/ML: Scikit-learn (Python ML stack)

---

## 1. Pendahuluan

### 1.1 Tujuan
Dokumen Software Requirements Specification (SRS) ini mendefinisikan kebutuhan fungsional dan non-fungsional untuk sistem **AutoPartSmart**[cite: 1]. Dokumen ini menjadi acuan verifikasi dan validasi pengembang serta penguji dalam membangun sistem peramalan permintaan suku cadang otomotif dan optimasi persediaan berbasis web[cite: 1].

### 1.2 Scope (Cakupan System)
Sistem **AutoPartSmart** mencakup:
* Pengelolaan dan pengunggahan data transaksi penjualan suku cadang bulanan dalam format CSV[cite: 1].
* Ekstraksi dan rekayasa fitur data (*feature engineering*) menggunakan fitur *lag* (Lag 1, Lag 2, Lag 3)[cite: 1].
* Eksekusi peramalan permintaan suku cadang bulanan berbasis algoritma Machine Learning (KNN & SVM Hybrid)[cite: 1].
* Perhitungan otomatis *safety stock* dan batas minimum persediaan[cite: 1].
* Visualisasi tren peramalan serta penyediaan data statistik deskriptif suku cadang[cite: 1].

Sistem **TIDAK** mencakup transaksi kasir/Point of Sale (POS), e-commerce/jual-beli suku cadang, pengadaan otomatis ke *supplier*, dan aplikasi *mobile native*.

### 1.3 Definisi Istilah
| Istilah | Definisi |
| :--- | :--- |
| **KNN (K-Nearest Neighbors)** | Algoritma *machine learning* berbasis jarak untuk memprediksi nilai berdasarkan kedekatan data historis[cite: 1]. |
| **SVM (Support Vector Machine)** | Algoritma *machine learning* regresi/klasifikasi untuk memetakan data non-linier[cite: 1]. |
| **Fitur Lag** | Nilai histori permintaan pada periode bulan sebelumnya ($t-1, t-2, t-3$) yang digunakan sebagai input prediktor[cite: 1]. |
| **SMAPE** | *Symmetric Mean Absolute Percentage Error*, metrik untuk mengukur tingkat kesalahan peramalan dalam persentase[cite: 1]. |
| **MAPE** | *Mean Absolute Percentage Error*, persentase rata-rata kesalahan absolut peramalan[cite: 1]. |
| **Safety Stock** | Persediaan pengaman tambahan untuk mengantisipasi lonjakan permintaan atau keterlambatan pasokan[cite: 1]. |

---

## 2. Deskripsi Umum

### 2.1 User & Stakeholder
1. **Manager Persediaan / Kepala Bengkel:** Mengunggah data histori, menjalankan modul peramalan, melihat grafik tren, dan mengeksekusi rekomendasi *safety stock*[cite: 1].
2. **Staf Gudang:** Mengunggah berkas transaksi harian/bulanan (CSV) dan melihat status ketersediaan barang[cite: 1].
3. **Pemilik Bengkel:** Mengakses laporan ringkasan statistik dan evaluasi akurasi stok[cite: 1].

### 2.2 Lingkungan Operasi
* **Platform Web:** Cross-browser compatible (Google Chrome v110+, Mozilla Firefox v110+, Safari v16+).
* **Environment Server:** Linux/Ubuntu Server, Python 3.10 runtime environment, PostgreSQL 15+.
* **Akses Pengguna:** Perangkat Desktop/Laptop dengan resolusi layar minimal $1280 \times 720$.

### 2.3 Asumsi & Dependensi
* **[ASUMSI-01]** Pengguna menyediakan berkas CSV dengan data histori penjualan bulanan minimal 12–24 periode bulan[cite: 1].
* **[ASUMSI-02]** Format berkas CSV memiliki struktur kolom minimal: Kode Barang, Nama Barang, Periode (Bulan-Tahun), dan Kuantitas Terjual[cite: 1].
* **[ASUMSI-03]** Server memiliki alokasi memori yang cukup untuk melakukan *batch processing* inferensi ML tanpa mengganggu performa respons HTTP[cite: 1].
* **[DEPENDENSI-01]** Ketersediaan *library* Python Machine Learning (Scikit-learn, Pandas, NumPy) yang stabil pada lingkungan server backend[cite: 1].

---

## 3. Kebutuhan Fungsional (Functional Requirements)

*Pola Penulisan: Sistem harus dapat `<aksi>` `<objek>` saat `<kondisi>` $\rightarrow$ `<output>`*

| ID | Kebutuhan Fungsional (FR) | Prioritas (MoSCoW) | Metode Verifikasi |
| :--- | :--- | :--- | :--- |
| **FR-01** | Sistem harus dapat **menerima dan memvalidasi struktur berkas CSV transaksi** saat **pengguna mengunggah berkas data histori penjualan** $\rightarrow$ Menampilkan status validasi sukses atau daftar pesan kesalahan format jika data tidak sesuai[cite: 1]. | **Must-Have** | Inspection & Demonstration |
| **FR-02** | Sistem harus dapat **mengekstraksi dan membentuk fitur lag (Lag 1, Lag 2, Lag 3)** saat **data transaksi bulanan bersih berhasil diproses oleh backend** $\rightarrow$ Matriks dataset yang siap diinferensi oleh model ML[cite: 1]. | **Must-Have** | Test Cases (Unit Test) |
| **FR-03** | Sistem harus dapat **menjalankan peramalan permintaan suku cadang bulanan menggunakan model KNN** saat **pengguna memicu proses peramalan** $\rightarrow$ Nilai kuantitas prediksi suku cadang untuk periode bulan berikutnya ($t+1$)[cite: 1]. | **Must-Have** | Test Cases (Integration Test) |
| **FR-04** | Sistem harus dapat **menghitung nilai safety stock suku cadang secara otomatis** saat **peramalan permintaan selesai dihitung** $\rightarrow$ Nilai rekomendasi batas minimum persediaan untuk tiap kode barang[cite: 1]. | **Must-Have** | Calculation Inspection |
| **FR-05** | Sistem harus dapat **menampilkan visualisasi grafik tren peramalan (histori vs prediksi)** saat **pengguna membuka halaman detail suku cadang** $\rightarrow$ Tampilan grafik garis interaktif pada antarmuka web[cite: 1]. | **Must-Have** | Demonstration |
| **FR-06** | Sistem harus dapat **menjalankan peramalan dengan model Hybrid Ensemble (SVM + KNN)** saat **pengguna memilih opsi metode peramalan lanjutan** $\rightarrow$ Nilai prediksi kombinasi dengan batas eror yang teroptimasi[cite: 1]. | **Should-Have** | Test Cases (Integration Test) |
| **FR-07** | Sistem harus dapat **menghitung statistik deskriptif (Rata-rata/Mean, Minimum, Maksimum, Standar Deviasi)** saat **pengguna membuka modul analisis data suku cadang** $\rightarrow$ Tabel ringkasan statistik persediaan[cite: 1]. | **Should-Have** | Calculation Inspection |
| **FR-08** | Sistem harus dapat **menampilkan notifikasi peringatan stok kritis (*Low Stock Alert*)** saat **stok riil berada di bawah nilai safety stock** $\rightarrow$ Indikator warna merah dan rincian barang pada dashboard[cite: 1]. | **Should-Have** | Demonstration |
| **FR-09** | Sistem harus dapat **menyediakan fitur penyesuaian nilai peramalan manual (*Manual Override*)** saat **pengguna mengidentifikasi faktor eksternal non-historis** $\rightarrow$ Angka proyeksi persediaan yang diperbarui sesuai input manual user. | **Should-Have** | System Test |

---

## 4. Kebutuhan Non-Fungsional (Non-Functional Requirements)

*Mengacu pada Karakteristik Kualitas ISO/IEC 25010*

| ID | Kategori ISO/IEC 25010 | Metrik | Target Kinerja | Kondisi Pengukuran | Metode Verifikasi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **NFR-01** | **Functional Suitability** *(Akurasi AI)* | SMAPE (*Symmetric Mean Absolute Percentage Error*)[cite: 1] | **SMAPE $< 10\%$** (khususnya model KNN dengan fitur lag)[cite: 1]. | Dievaluasi menggunakan dataset ujipengisian 33 bulan pada item sporadis[cite: 1]. | Data Analysis Test |
| **NFR-02** | **Performance Efficiency** *(Latensi AI)* | Waktu Respons Inferensi AI | **$< 3.0$ detik** per *batch* 100 suku cadang. | Pengujian *batch inference* pada server backend berpesifikasi standar. | Performance Benchmark |
| **NFR-03** | **Performance Efficiency** *(Latensi UI)* | Page Load Time & Response Time | **$< 2.0$ detik** untuk pemuatan halaman dashboard utama. | Koneksi jaringan lokal/broadband $\ge 10$ Mbps dengan 10 *concurrent users*. | Benchmark Tool (Lighthouse/JMeter) |
| **NFR-04** | **Usability** | System Usability Scale (SUS) & Error Rate | **Skor SUS $\ge 75$**; Tingkat kegagalan tugas impor CSV $< 5\%$. | Uji keterpakaian (*usability testing*) pada 5-10 sampel pengguna bengkel. | Usability Survey & Logging |
| **NFR-05** | **Security** | Otentikasi & Perlindungan Data | Encrypted Session Tokens (JWT), Password Hashing (bcrypt/Argon2), Sanitasi Input CSV. | Pengujian simulasi *SQL Injection* dan *XSS Attack* pada form *upload*. | Security Audit / Pen-Test |
| **NFR-06** | **Privacy** | Akses & Isolasi Data | Data transaksi bengkel terisolasi (*multi-tenant isolation*); Tidak ada pembocoran data antar ID bengkel. | Pengujian akses kontrol API menggunakan *unauthorized token*. | Inspection & Security Test |
| **NFR-07** | **Reliability** *(Fallback Mechanism)* | Graceful Degradation / Fallback Rate | **100% ketersediaan prediksi cadangan** (*Moving Average*) saat engine ML mengalami kegagalan/error. | Simulasi penghentian (*shutdown*) modul ML backend secara mendadak. | Fault Injection Test |

---

## 5. Kebutuhan Data Minimum Fitur AI

### 5.1 Skema Input Model (Feature Vector)
Untuk menghasilkan peramalan periode bulan $t$, model memerlukan data masukan terstruktur berikut[cite: 1]:
* **Identitas Barang:** `item_code` (String / Categorical)[cite: 1].
* **Fitur Lag 1 ($t-1$):** `lag_1` (Float/Integer) — Jumlah penjualan suku cadang 1 bulan sebelum periode prediksi[cite: 1].
* **Fitur Lag 2 ($t-2$):** `lag_2` (Float/Integer) — Jumlah penjualan suku cadang 2 bulan sebelum periode prediksi[cite: 1].
* **Fitur Lag 3 ($t-3$):** `lag_3` (Float/Integer) — Jumlah penjualan suku cadang 3 bulan sebelum periode prediksi[cite: 1].
* **Statistik Historis (Rolling Window):** `moving_std_3` (Float) — Standar deviasi penjualan 3 bulan terakhir[cite: 1].

### 5.2 Skema Output Model
* **Kuantitas Prediksi ($\hat{Y}_t$):** `predicted_quantity` (Float, dibulatkan ke Integer non-negatif $\ge 0$) — Proyeksi unit suku cadang yang akan dibutuhkan pada bulan $t$[cite: 1].
* **Interval Estimasi Eror:** `estimated_error_margin` (Float) — Proyeksi batas eror berdasarkan histori MAPE/SMAPE item terkait[cite: 1].
* **Safety Stock ($SS$):** `recommended_safety_stock` (Integer) — Hasil kalkulasi batas pengaman stok[cite: 1].

---

## 6. Aturan Bisnis (Business Rules) Hasil Riset

1. **BR-01 (Batasan Prediksi Non-Negatif):** Nilai prediksi kuantitas permintaan suku cadang tidak boleh bernilai negatif ($\hat{Y}_t \ge 0$). Jika model menghasilkan nilai $< 0$ (seperti pada kelemahan metode SARIMA), sistem harus secara otomatis membulatkan nilai menjadi $0$[cite: 1].
2. **BR-02 (Metode Peramalan Utama):** Algoritma berbasis KNN dengan rekayasa fitur *Lag 1, Lag 2, Lag 3* diprioritaskan sebagai metode *default* utama karena terbukti menghasilkan error terendah pada pola permintaan sporadis (MAPE 7,31% & SMAPE 7,63%)[cite: 1].
3. **BR-03 (Formula Perhitungan Safety Stock):** Perhitungan *Safety Stock* wajib memperhitungakn variabilitas permintaan (Standar Deviasi) dari data histori dan *lead time* pasokan baku untuk mencegah *stockout*[cite: 1].
4. **BR-04 (Penanganan Data Kosong/Zero Demand):** Periode bulan tanpa transaksi penjualan tidak boleh diabaikan atau dihapus, melainkan diisi dengan nilai `0` (*zero-imputation*) untuk menjaga kontinuitas deret waktu fitur *lag*[cite: 1].

---

## 7. Matriks Ketertelusuran (Traceability Matrix)

| ID Kebutuhan (FR / NFR) | Fitur PRD Terkait | Rumusan Masalah / Bukti Riset Terkait |
| :--- | :--- | :--- |
| **FR-01** | Impor & Manajemen Data Transaksi | Penanganan *dataset* transaksi bulanan bengkel[cite: 1]. |
| **FR-02** | Fitur AI Prediksi (Preprocessing) | Pembuatan fitur *lag* ($t-1, t-2, t-3$) untuk menangkap pola lokal[cite: 1]. |
| **FR-03** | Fitur AI Prediksi Permintaan Bulanan | Mengatasi fluktuasi ekstrem suku cadang dengan algoritma KNN[cite: 1]. |
| **FR-04** | Modul Otomatisasi *Safety Stock* | Mencegah terjadinya *stockout* dan penumpukan *overstock*[cite: 1]. |
| **FR-05** | Visualisasi Tren Permintaan | Kebutuhan antarmuka grafik interaktif untuk analisis pengguna[cite: 1]. |
| **FR-06** | Fitur AI Hybrid Ensemble (SVM + KNN) | Penggabungan keunggulan model KNN & SVM[cite: 1]. |
| **FR-07** | Eksplorasi Data & Deskripsi Statistik | Kebutuhan ringkasan variabel statistik (Mean, Min, Max, Std Dev)[cite: 1]. |
| **FR-08** | Peringatan Stok Kritis (*Low Stock Alert*) | Indikator peringatan dini sebelum terjadi *stockout*[cite: 1]. |
| **FR-09** | Penyesuaian Manual (*Manual Override*) | Mitigasi risiko faktor eksternal non-historis[cite: 1]. |
| **NFR-01** | Akurasi AI (SMAPE $< 10\%$) | Kegagalan metode konvensional SARIMA (SMAPE 28,23%) vs Keunggulan ML[cite: 1]. |
| **NFR-02** | Latensi Inferensi AI | Batasan efisiensi komputasi *cloud* dan pengalaman pengguna[cite: 1]. |
| **NFR-03** | Latensi Pemuatan Dashboard | Standar kenyamanan pengguna berbasis web[cite: 1]. |
| **NFR-04** | Usability (Skor SUS $\ge 75$) | Kemudahan pengoperasian oleh Manager Persediaan (Pak Budi)[cite: 1]. |
| **NFR-05 & NFR-06** | Keamanan & Privasi Data | Perlindungan data transaksi dan privasi antar-bengkel[cite: 1]. |
| **NFR-07** | Reliability (Fallback Engine) | Jaminan ketersediaan layanan saat modul ML berhalangan[cite: 1]. |
