# Acceptance Criteria & Test Scenarios - AutoPartSmart

**Versi:** 1.0  
**Tanggal:** 19 September 2026  
**Peran:** QA Engineer & Test Analyst  
**Platform:** Website  

---

## 1. Draf Acceptance Criteria (Format Gherkin)

### US-01: Validasi dan Unggah Berkas CSV Transaksi
* **Kategori:** Fitur Inti (Must-Have)
* **Metode Uji:** Unit Test (Parser/Validator) & System Integration Test (SIT)

```gherkin
Scenario: Mengunggah berkas CSV transaksi dengan struktur yang valid
  Given Staf Gudang telah memilih berkas "penjualan_2024.csv" dengan struktur kolom wajib (item_code, period, qty)
  When Staf Gudang menekan tombol "Unggah CSV"
  Then Sistem berhasil menyimpan data transaksi ke database
  And Sistem menampilkan notifikasi sukses "Data transaksi berhasil diimpor" dalam waktu <= 2.0 detik

Scenario: Mengunggah berkas CSV dengan nama kolom yang salah (Edge Case)
  Given Staf Gudang memilih berkas "penjualan_salah.csv" di mana kolom "qty" terkeliru menjadi "jumlah"
  When Staf Gudang menekan tombol "Unggah CSV"
  Then Sistem membatalkan proses impor ke database
  And Sistem menampilkan pesan kesalahan "Kolom wajib 'qty' tidak ditemukan pada berkas CSV"
