# Product Requirement Document (PRD)

**Nama Produk:** AutoPartSmart (Sistem Peramalan Permintaan & Optimasi Persediaan Suku Cadang Otomotif)  
**Versi:** 1.0  
**Tanggal:** 19 September 2026  
**Penulis:** Senior Product Manager (AI/Mobile & Web)  

---

## 1. Ringkasan Eksekutif

**AutoPartSmart** adalah sistem manajemen persediaan suku cadang otomotif berbasis platform **Web** yang mengintegrasikan fitur prediksi berbasis kecerdasan buatan (*Machine Learning*). Produk ini dirancang untuk mengatasi masalah ketidakseimbangan stok—seperti *overstock* dan *stockout*—akibat pola permintaan suku cadang yang sporadis dan tidak stabil. Menggunakan pendekatan model ML (*K-Nearest Neighbors* / *Support Vector Machine*) dengan teknik *feature engineering* (fitur *lag*), produk ini memberikan peramalan permintaan bulanan yang akurat serta rekomendasi kuantitas *safety stock* secara otomatis untuk meningkatkan efisiensi operasional dan rantai pasok bengkel.

---

## 2. Problem Statement & Bukti

### Problem Statement
Pengelola bengkel dan tim *supply chain* kesulitan menentukan kuantitas pengadaan suku cadang otomotif secara akurat karena pola permintaan bersifat sporadis, fluktuatif, dan tidak mengikuti pola musiman linier, yang mengakibatkan tingginya biaya penyimpanan persediaan (*overstock*) serta hilangnya potensi penjualan (*stockout*).

### Bukti (Fakta vs Asumsi)

* **Fakta (Berdasarkan Data Riset / Dataset 33 Bulan):**
  * Permintaan suku cadang sangat berfluktuasi dan sporadis (contoh: item `A-04000-081B0` berfluktuasi ekstrem antara 1 hingga 10 unit per bulan).
  * Metode statistik konvensional (SARIMA) memiliki akurasi terendah dengan tingkat kesalahan tertinggi ($\text{SMAPE } 28,23\%$ & $\text{MAPE } 33,91\%$), bahkan memprediksi kuantitas bernilai negatif yang tidak realistis secara fisik.
  * Algoritma *Machine Learning* terbukti paling akurat dalam menangkap fluktuasi lokal, dengan model KNN menghasilkan error terendah ($\text{MAPE } 7,31\%$ & $\text{SMAPE } 7,63\%$).
* **Asumsi:**
  * **[ASUMSI-01]** Pengguna di bengkel/distributor telah memiliki sistem pencatatan transaksi penjualan internal yang dapat diekspor ke dalam format CSV/Excel.
  * **[ASUMSI-02]** Biaya kerugian akibat *stockout* dan penumpukan *overstock* saat ini menyedot hingga 15–20% dari margin operasional bulanan bengkel.

---

## 3. Target User & Stakeholder

| Pemangku Kepentingan / Peran | Kebutuhan Utama | Pengaruh & Dampak (Tinggi/Sedang/Rendah) |
| :--- | :--- | :--- |
| **Manager Persediaan / Kepala Bengkel** *(Target User Utama)* | Memprediksi kebutuhan suku cadang secara akurat dan mendapat rekomendasi jumlah *safety stock* berbasis data untuk periode berikutnya. | **Tinggi** (Pengambil keputusan utama pengadaan & pengguna harian platform). |
| **Staf Gudang & Penjualan** *(Target User Sekunder)* | Kemudahan mengunggah data transaksi (CSV) dan memantau status stok barang secara *real-time*. | **Sedang** (Penginput data harian & eksekutor operasional). |
| **Pemilik Bengkel / Manajemen Senior** | Penurunan biaya operasional persediaan, reduksi *dead stock*, serta peningkatan kepuasan pelanggan. | **Tinggi** (Penyedia anggaran & penentu keberhasilan ROI). |
| **Tim Developer & AI Engineer** | Alur integrasi API model Machine Learning yang efisien, responsif, dan hemat biaya komputasi server. | **Sedang** (Pembangun teknis produk). |

### Persona Ringkas
* **Nama:** Pak Budi (42 tahun)
* **Jabatan:** Manager Persediaan Bengkel Otomotif
* **Karakteristik:** Memiliki latar belakang operasional, terbiasa menggunakan aplikasi web sederhana, namun tidak memahami teori teknis *Machine Learning*. Menyukai visualisasi grafik ringkas dan rekomendasi angka yang siap dieksekusi.

---

## 4. Value Proposition

* **Pain yang Dikurangi:**
  * Menghilangkan risiko *human-error* dan keraguan berbasis insting subjektif dalam melakukan *restock* barang.
  * Mengurangi penumpukan modal berlebih akibat *overstock* suku cadang yang jarang laku.
  * Meminimalkan risiko kekecewaan pelanggan akibat *stockout* saat serviks/perbaikan.
* **Gain yang Diciptakan:**
  * *Dashboard* peramalan otomatis berbasis bulanan dengan visualisasi yang mudah dipahami.
  * Rekomendasi otomatis batas minimum persediaan (*Safety Stock*) untuk mencegah kehabisan stok mendadak.
* **Mengapa Fitur AI Bukan Gimmick:**
  Pola permintaan suku cadang bersifat *intermittent* (terputus-putus) dan non-linier. Rumus perataan sederhana atau metode linier tradisional (seperti SARIMA) gagal memprediksi pola bergelombang ini. Model AI (*K-Nearest Neighbors* / *Support Vector Machine*) terbukti secara empiris mampu menurunkan tingkat kesalahan prediksi (*error rate*) hingga di bawah 8% melalui pemanfaatan fitur *lag* historis.

---

## 5. Tujuan Produk & KPI Terukur

| Tujuan Produk | KPI Terukur | Cara Mengukur |
| :--- | :--- | :--- |
| **Meningkatkan Akurasi Prediksi** | Nilai $\text{SMAPE}$ model prediksi bulanan $< 10\%$. | Membandingkan angka peramalan AI dengan data aktual penjualan bulanan di akhir periode. |
| **Mengurangi Risiko Stockout** | Penurunan insiden kehabisan stok (*stockout*) sebesar 25–30%. | Menghitung frekuensi penolakan transaksi akibat stok kosong melalui log sistem. |
| **Adopsi Pengguna Bengkel** | $> 80\%$ Pengguna Aktif Bulanan (*Monthly Active Users*) menerapkan angka rekomendasi persediaan AI. | Mengukur tingkat interaksi tombol *"Terapkan Rekomendasi Restock"* pada platform web. |

---

## 6. Scope Fitur 3 Bulan (Tabel MoSCoW)

| Kategori | Fitur / Spesifikasi |
| :--- | :--- |
| **Must-Have** | • Manajemen & Impor Data Transaksi (Support unggah format `.csv`).<br>• ★ **Fitur AI Prediksi Permintaan Bulanan (Model KNN berbasis fitur Lag 1, 2, dan 3)**.<br>• Visualisasi Grafik Tren Permintaan (Komparasi data historis vs hasil prediksi).<br>• Modul Otomatisasi Perhitungan *Safety Stock*. |
| **Should-Have** | • ★ **Fitur AI Ensemble Hybrid (Kombinasi SVM + KNN)**.<br>• Dashboard Eksplorasi Data & Statistik Deskriptif Stok (Mean, Min, Max, Std Dev).<br>• Peringatan Dini Stok Kritis (*Low Stock Alert Notification*). |
| **Could-Have** | • Ringkasan *Business Intelligence* untuk Manajemen / Pemilik Bengkel.<br>• Ekspor Laporan Peramalan ke format `.pdf` atau `.xlsx`. |
| **Won't-Have (Periode Ini)** | • Integrasi otomatis API *real-time* ke sistem kasir/POS pihak ketiga.<br>• Pengembangan aplikasi Mobile Native (fokus penuh pada Web responsif).<br>• Otomatisasi pemesanan langsung ke *supplier* (*auto-ordering*). |

*(Keterangan: Fitur bertanda ★ merupakan fitur berbasis AI utama)*

---

## 7. Non-Goals Eksplisit

* **Bukan Sistem Point of Sale (POS) / Kasir:** Produk tidak dirancang untuk memproses transaksi kasir langsung di meja kasir.
* **Bukan Platform Marketplace / E-Commerce:** Produk tidak menyediakan fasilitasi jual-beli suku cadang antar-bengkel atau distributor.
* **Tidak Melakukan Eksekusi Pembelian Otomatis:** Produk hanya memberikan rekomendasi angka pengadaan; keputusan pembelian tetap dilakukan secara manual oleh user.

---

## 8. Asumsi, Risiko Utama & Mitigasi

| Kode / Risiko | Deskripsi Risiko / Asumsi | Tingkat Risiko | Strategi Mitigasi |
| :--- | :--- | :--- | :--- |
| **[ASUMSI-03]** | Data histori penjualan bulanan minimal 12–24 bulan tersedia dan valid untuk diolah model ML. | **Tinggi** | Implementasikan prosedur *data preprocessing* (imputasi nilai hilang) dan manfaatkan algoritma KNN yang stabil pada sampel data terbatas. |
| **[ASUMSI-04]** | Anggaran komputasi server *cloud* terbatas selama masa prototipe 1 semester. | **Sedang** | Jalankan proses *inference/training* model secara berkala (*batch processing* bulanan) untuk menekan biaya operasional API/server. |
| **Risiko Data Format** | Format file CSV yang diunggah pengguna tidak konsisten atau memiliki banyak nilai kosong. | **Tinggi** | Sediakan berkas *template* CSV standar serta mekanisme validasi format di sisi *front-end* sebelum file diproses. |
| **Risiko Eksternal** | Terjadi lonjakan permintaan mendadak akibat faktor eksternal yang tidak tercatat dalam histori (misal: kebijakan *recall*). | **Sedang** | Sediakan fitur *Manual Override* agar Manager Persediaan dapat menyesuaikan angka prediksi AI secara manual. |