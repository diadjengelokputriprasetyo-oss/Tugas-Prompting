# User Stories & Agile Requirements Documentation - AutoPartSmart

**Nama Produk:** AutoPartSmart (Sistem Peramalan Permintaan & Optimasi Persediaan Suku Cadang Otomotif)[cite: 1]  
**Versi:** 1.0  
**Tanggal:** 19 September 2026  
**Peran:** Agile Product Owner, System Analyst, & QA Engineer  
**Persona Utama:** Pak Budi (Manager Persediaan Bengkel) & Staf Gudang  
**Platform:** Website  

---

## 1. Daftar User Stories (Prioritas Must & Should)

| ID Story | Narasi User Story | FR Asal | Prioritas | Kategori |
| :--- | :--- | :--- | :--- | :--- |
| **US-01** | **Sebagai** Staf Gudang, **saya ingin** mengunggah berkas CSV transaksi penjualan bulanan dan menerima pesan error jika formatnya salah, **agar** data transaksi yang masuk ke sistem valid dan tidak merusak proses perhitungan stok[cite: 1]. | FR-01 | Must-Have | Fitur Inti |
| **US-02** | **Sebagai** Manager Persediaan, **saya ingin** sistem menyiapkan fitur historis penjualan (Lag 1, 2, 3) secara otomatis setelah data CSV diunggah, **agar** dataset siap diproses oleh model prediksi tanpa perlu diolah manual[cite: 1]. | FR-02 | Must-Have | Fitur AI ★ |
| **US-03** | **Sebagai** Manager Persediaan, **saya ingin** melihat hasil peramalan jumlah suku cadang bulan depan berbasis model KNN, **agar** saya dapat menentukan kuantitas pengadaan barang secara akurat dan tidak menebak-nebak[cite: 1]. | FR-03 | Must-Have | Fitur AI ★ |
| **US-04** | **Sebagai** Manager Persediaan, **saya ingin** mendapatkan angka rekomendasi *safety stock* otomatis untuk setiap suku cadang, **agar** bengkel memiliki batas aman persediaan untuk mencegah kondisi kehabisan stok (*stockout*)[cite: 1]. | FR-04 | Must-Have | Fitur Inti |
| **US-05** | **Sebagai** Manager Persediaan, **saya ingin** melihat grafik perbandingan tren penjualan historis vs hasil prediksi, **agar** saya dapat menganalisis pergerakan permintaan barang secara cepat dan intuitif[cite: 1]. | FR-05 | Must-Have | Fitur Inti |
| **US-06** | **Sebagai** Manager Persediaan, **saya ingin** memilih opsi peramalan lanjutan berbasis algoritma Hybrid (SVM + KNN), **agar** saya memperoleh proyeksi stok dengan tingkat kesalahan (*error rate*) yang lebih stabil pada barang berfluktuasi tinggi[cite: 1]. | FR-06 | Should-Have | Fitur AI ★ |
| **US-07** | **Sebagai** Manager Persediaan, **saya ingin** melihat ringkasan statistik suku cadang (Rata-rata, Min, Max, Standar Deviasi), **agar** saya dapat mengidentifikasi pola variabilitas permintaan tiap jenis barang[cite: 1]. | FR-07 | Should-Have | Fitur Inti |
| **US-08** | **Sebagai** Manager Persediaan, **saya ingin** melihat indikator peringatan warna merah pada *dashboard* saat stok riil berada di bawah *safety stock*, **agar** saya dapat segera melakukan order ulang sebelum barang habis[cite: 1]. | FR-08 | Should-Have | Fitur Inti |
| **US-09** | **Sebagai** Manager Persediaan, **saya ingin** menyesuaikan (*override*) angka hasil prediksi AI secara manual, **agar** saya dapat memasukkan faktor luar (seperti tren modifikasi mendadak atau *event* promosi) yang tidak terekam pada data histori[cite: 1]. | FR-09 | Should-Have | Fitur Inti |

### Dekomposisi Epic (Pemecahan Story Besar AI)
Jika kebutuhan peramalan AI utama (**US-03**) terlalu kompleks untuk dikerjakan dalam 1 *sprint*, *story* ini dipecah menjadi 3 sub-story:
1. **US-03A (Pra-pemrosesan Data AI):** **Sebagai** Manager Persediaan, **saya ingin** sistem mengisi nilai `0` secara otomatis pada periode bulan tanpa transaksi (*zero-imputation*), **agar** deret waktu fitur *lag* tidak terputus saat dihitung oleh model Machine Learning[cite: 1].
2. **US-03B (Inferensi Prediksi AI):** **Sebagai** Manager Persediaan, **saya ingin** sistem menghasilkan nilai kuantitas prediksi suku cadang bulan berikutnya berbasis algoritma KNN, **agar** saya mendapatkan proyeksi kebutuhan stok berbasis data historis[cite: 1].
3. **US-03C (Guardrail / Pembulatan Prediksi):** **Sebagai** Manager Persediaan, **saya ingin** sistem otomatis membulatkan nilai prediksi yang bernilai negatif menjadi `0`, **agar** angka rekomendasi persediaan tetap logis secara bisnis[cite: 1].

---

## 2. Rincian Use Cases

### UC-01: Menjalankan Peramalan Permintaan Suku Cadang Bulanan (Fitur AI ★)
* **Aktor Utama:** Manager Persediaan (Pak Budi)[cite: 1]
* **Aktor Pendukung:** Backend AI Inference Engine (Model ML KNN & SVM Hybrid), Database System (PostgreSQL)[cite: 1]
* **Kaitan ID Story & FR:** US-02, US-03, US-04, US-06 | FR-02, FR-03, FR-04, FR-06[cite: 1]

#### Preconditions
1. Pengguna berhasil *login* ke sistem.
2. Data transaksi histori penjualan suku cadang bulanan (minimal 12–24 bulan) sudah tersedia di Database[cite: 1].

#### Postconditions
1. Sistem menampilkan hasil angka peramalan kuantitas suku cadang bulan depan ($\hat{Y}_{t+1}$) beserta estimasi *safety stock*[cite: 1].
2. Hasil peramalan tersimpan di database log prediksi[cite: 1].

#### Alur Utama (Main Flow)
1. Manager Persediaan memilih kode/kategori suku cadang dan metode peramalan (KNN Standar / Hybrid SVM-KNN)[cite: 1].
2. Manager Persediaan menekan tombol untuk memicu eksekusi peramalan[cite: 1].
3. Sistem mengambil data transaksi histori suku cadang dari Database.
4. Sistem mengekstraksi *feature engineering* (vektor *Lag 1, Lag 2, Lag 3* dan *Moving Standard Deviation*)[cite: 1].
5. Sistem mengirimkan matriks vektor fitur ke Backend AI Inference Engine[cite: 1].
6. AI Inference Engine menghitung nilai prediksi kuantitas permintaan menggunakan model terlatih[cite: 1].
7. AI Inference Engine mengembalikan nilai prediksi kuantitas dan estimasi eror ke sistem[cite: 1].
8. Sistem menghitung rekomendasi *safety stock* berbasis standar deviasi dan *lead time*[cite: 1].
9. Sistem menerapkan aturan bisnis *guardrail*: membulatkan nilai negatif menjadi `0`[cite: 1].
10. Sistem menampilkan hasil kuantitas peramalan, *safety stock*, dan grafik tren di layar[cite: 1].
11. Sistem menyimpan riwayat hasil prediksi ke Database.

#### Alur Eksepsi Khusus AI (AI Exception Flows)
* **EX-01: Data Histori Kurang (< 3 Bulan)**
  1. On langkah 4, sistem mendeteksi jumlah deret waktu $< 3$ bulan[cite: 1].
  2. Sistem membatalkan pengiriman ke AI Inference Engine.
  3. Sistem menampilkan peringatan: *"Data histori penjualan kurang dari 3 bulan. Peramalan AI tidak dapat dijalankan."*[cite: 1]
  4. Sistem mengaktifkan *fallback mode*: Menghitung prediksi menggunakan *Simple Moving Average*[cite: 1].
* **EX-02: Timeout atau Gagal Koneksi ke Engine AI (> 3.0 Detik)**
  1. On langkah 5 atau 6, sistem tidak menerima respons dari AI Inference Engine dalam waktu 3.0 detik (NFR-02)[cite: 1].
  2. Sistem mencatat log *error connection/timeout*.
  3. Sistem menampilkan notifikasi *banner*: *"Layanan AI tidak merespons. Menampilkan estimasi berdasarkan metode cadangan."*[cite: 1]
  4. Sistem menjalankan algoritma *fallback* (*Moving Average 3 Bulanan*) secara lokal (*Graceful Degradation*)[cite: 1].
* **EX-03: Confidence Rendah / Variabilitas Tinggi ($\text{SMAPE} > 25\%$)**
  1. On langkah 7, AI Inference Engine mengembalikan hasil prediksi dengan bendera `low_confidence = True`[cite: 1].
  2. Sistem tetap menampilkan hasil peramalan di layar disertai *warning badge*: *"Variabilitas Tinggi"*[cite: 1].
  3. Sistem mengaktifkan tombol penyesuaian manual (*Manual Override*)[cite: 1].

---

### UC-02: Melakukan Validasi dan Preprocessing Data Transaksi CSV
* **Aktor Utama:** Staf Gudang / Manager Persediaan[cite: 1]
* **Aktor Pendukung:** Database System (PostgreSQL)
* **Kaitan ID Story & FR:** US-01, US-02 | FR-01, FR-02[cite: 1]

#### Preconditions
Pengguna memiliki berkas CSV data penjualan suku cadang bulanan[cite: 1].

#### Postconditions
Data transaksi tervalidasi, nilai *missing/zero* ditangani, dan tersimpan di database[cite: 1].

#### Alur Utama (Main Flow)
1. Staf Gudang memilih dan mengunggah berkas CSV ke dalam sistem[cite: 1].
2. Sistem memeriksa format berkas, nama kolom wajib, dan tipe data.
3. Sistem mendeteksi periode bulan kosong (*zero demand*) dan melakukan *zero-imputation* (mengisi `0`)[cite: 1].
4. Sistem menyimpan data transaksi terstruktur ke dalam Database.
5. Sistem menampilkan konfirmasi sukses beserta ringkasan baris data yang diimpor[cite: 1].

#### Alur Eksepsi
* **EX-01: Struktur Berkas CSV Salah / Rusak**
  1. On langkah 2, sistem mendeteksi kolom wajib (misal `qty`) tidak ditemukan[cite: 1].
  2. Sistem membatalkan proses impor dan menampilkan daftar rincian kolom yang salah[cite: 1].

---

## 3. Diagram Alur Pengguna (User Flow)

```mermaid
flowchart TD
    %% Titik Masuk
    A([Titik Masuk: Menu Peramalan Stok]) --> B[Pengguna Pilih Suku Cadang & Metode AI]
    
    %% Status 1: Validasi Awal (Client-Side)
    B --> C{Validasi Lokal: Data Histori >= 3 Bulan?}
    C -- Tidak --> C1[Tampilkan Tooltip: Data Histori Kurang] --> B
    C -- Ya --> D[Pengguna Klik 'Jalankan Peramalan']
    
    %% Status 2: Indikator Pemrosesan
    D --> E[Tampilkan Loading Spinner & Status 'Menganalisis Data...']
    E --> F{Request Backend AI}
    
    %% Status 4: Fallback Engine
    F -- Timeout > 3s / Server Error --> G[Tampilkan Banner: AI Fallback Active]
    G --> H[Hitung Prediksi dengan Simple Moving Average]
    H --> I[Tampilkan Hasil Prediksi Cadangan]
    
    %% Status 3: Penanganan Hasil AI
    F -- Sukses Responsive --> J{Cek Confidence Level / SMAPE}
    J -- Low Confidence (SMAPE > 25%) --> K[Tampilkan Warning Badge 'Variabilitas Tinggi']
    K --> L[Tampilkan Grafik & Hasil Prediksi]
    L --> M[Aktifkan Opsi Manual Override]
    
    J -- High Confidence (SMAPE <= 25%) --> N[Tampilkan Badge Hijau 'Akurasi Tinggi']
    N --> O[Tampilkan Grafik, Prediksi & Safety Stock]
    
    %% Selesai
    I --> P([Selesai: Simpan / Gunakan Rekomendasi Stok])
    M --> P
    O --> P
