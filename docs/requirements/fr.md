# User Stories - AutoPartSmart

**Versi:** 1.0  
**Tanggal:** 19 September 2026  
**Peran:** Agile Product Owner & Business Analyst  
**Persona Utama:** Pak Budi (Manager Persediaan Bengkel) & Staf Gudang  
**Platform:** Website  

---

## 1. Tabel User Stories (Prioritas Must & Should)

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

---

## 2. Evaluasi Ringkas Prinsip INVEST

* **Independent (Independen):** Setiap *story* dirancang agar dapat dikembangkan secara terpisah. Contohnya, fitur visualisasi grafik (**US-05**) atau penyesuaian manual (**US-09**) dapat dikerjakan tanpa memblokir pengembangan mesin peramalan AI utama (**US-03**).
* **Negotiable (Dapat Dinegosiasikan):** *Story* memberikan fleksibilitas bagi tim pengembang untuk menentukan detail antarmuka atau metode pemrosesan backend selama kriteria penerimaan terpenuhi.
* **Valuable (Bernilai):** Seluruh *story* membawa dampak bisnis yang jelas, seperti membantu Pak Budi meminimalkan risiko *stockout* dan *overstock*[cite: 1], serta membantu Staf Gudang memastikan integritas data[cite: 1].
* **Estimable (Dapat Diestimasi):** Batasan fungsi dan cakupan data pada tiap *story* sudah jelas, sehingga tim teknis dapat memberikan estimasi ukuran/bobot kerja (*story points*).
* **Small (Kecil):** Ruang lingkup per *story* berada dalam skala yang ideal untuk diselesaikan dalam 1 iterasi *sprint* (1–2 minggu).
* **Testable (Dapat Diuji):** Setiap *story* dapat diverifikasi dengan kriteria penerimaan yang terukur mengacu pada metrik SRS (misalnya: ketiadaan nilai prediksi negatif, SMAPE $<10\%$, dan pesan kesalahan pada validasi CSV)[cite: 1].

---

## 3. Pemecahan Epic (Dekomposisi Story Besar)

Apabila kebutuhan peramalan AI utama (**US-03**) dinilai terlalu kompleks untuk dikerjakan dalam satu *sprint*, maka *story* tersebut dapat dipecah menjadi **3 story kecil yang berdiri sendiri**:

1. **US-03A (Pra-pemrosesan Data AI):**
   > **Sebagai** Manager Persediaan, **saya ingin** sistem mengisi nilai `0` secara otomatis pada periode bulan tanpa transaksi (*zero-imputation*), **agar** deret waktu fitur *lag* tidak terputus saat dihitung oleh model Machine Learning[cite: 1].
2. **US-03B (Inferensi Prediksi AI):**
   > **Sebagai** Manager Persediaan, **saya ingin** sistem menghasilkan nilai kuantitas prediksi suku cadang bulan berikutnya berbasis algoritma KNN, **agar** saya mendapatkan proyeksi kebutuhan stok berbasis data historis[cite: 1].
3. **US-03C (Guardrail / Aturan Pembulatan Prediksi):**
   > **Sebagai** Manager Persediaan, **saya ingin** sistem otomatis membulatkan nilai prediksi yang bernilai negatif menjadi `0`, **agar** angka rekomendasi persediaan tetap logis dan relevan dari sudut pandang bisnis[cite: 1].
