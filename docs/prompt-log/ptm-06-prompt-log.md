# Log Prompt Interaksi AI — PTM-06 (ptm-06-prompt-log)

**Mata Kuliah:** Intelligent Mobile and Web Application Development (IMWAD)  
**Pertemuan ke-:** 06 dari 16  
**Topik:** Implementasi Backend API, Validasi Masukan, Autentikasi JWT, dan Keamanan OWASP API  
**Mahasiswa / Tim:** Tim Pengembang AutoPartSmart  
**Semester / T.A.:** Ganjil 2025/2026  

---

## 1. Tabel Riwayat Prompt Wajib (Sesi Kelas & Mandiri)

| No | Target Prompt | Alat AI & Versi | Ringkasan Prompt | Kualitas Output (1-5) | Revisi Manual |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **D.1 Scaffold Modular** | Gemini 3.8 Flash (High) | Scaffold struktur 3 lapisan (Router $\rightarrow$ Service $\rightarrow$ Repository) berbasis `openapi.yaml` dan skema `erd.md` AutoPartSmart dengan koneksi SQLAlchemy aman. | **5** | Menyesuaikan model `users` dan `predictions` agar menggunakan UUID string 36-karakter yang kompatibel dengan SQLite dan PostgreSQL tanpa dependensi eksternal. |
| **2** | **D.2 Autentikasi JWT** | Gemini 3.8 Flash (High) | Implementasi OAuth2 Password Flow, password hashing bcrypt, token pair (Access Token 30m + Refresh Token 7d), protected endpoint `GET /auth/me`. | **4** | Memperbaiki dependensi hashing: mengganti mekanisme wrapper `passlib` versi lama yang mengalami isu `__about__.__version__` pada Python 3.13 menjadi pustaka native `bcrypt` modern. |
| **3** | **D.3 Audit OWASP & BOLA** | Gemini 3.8 Flash (High) | Audit OWASP API Security Top 10 (2023), penutupan celah BOLA pada `GET /predictions/{id}` dengan status 403 Forbidden, dan helper sanitasi masukan inferensi AI. | **5** | Menambahkan regex pattern komprehensif untuk *Prompt Injection* dan pembatasan query parameter paginasi `limit` (max 100) guna mencegah *Unrestricted Resource Consumption*. |
| **4** | **Iterasi Lanjutan (D.4)** | Gemini 3.8 Flash (High) | Perbaikan validasi masukan email Pydantic v2 dengan mengintegrasikan `email-validator` dan sinkronisasi route alias `POST /auth/signup` terhadap `POST /auth/register`. | **5** | Mengonfigurasi `model_config = ConfigDict(from_attributes=True)` sesuai standar Pydantic v2 untuk menghilangkan *deprecation warning*. |

---

## 2. Tabel Iterasi & Evaluasi Prompt

| Prompt | Masalah pada Output AI Pertama | Analisis Penyebab | Revisi / Prompt Lanjutan yang Digunakan | Hasil Pasca Perbaikan |
| :--- | :--- | :--- | :--- | :--- |
| **D.1 Scaffold Modular** | Inisialisasi koneksi database belum menangani argumen `check_same_thread=False` pada SQLite lokal. | SQLite secara default melarang akses multi-thread antar-request FastAPI jika thread pooling aktif. | Tambahkan kondisi: `if settings.DATABASE_URL.startswith("sqlite"): connect_args = {"check_same_thread": False}` | Database dapat diakses multi-thread secara aman tanpa koneksi terkunci (*database locked*). |
| **D.2 Autentikasi JWT** | Pustaka `passlib` 1.7.4 memicu `AttributeError: module 'bcrypt' has no attribute '__about__'` pada Python 3.13. | Pustaka `bcrypt` versi 4.1.0+ menghapus atribut internal `__about__`, sedangkan `passlib` tidak lagi diperbarui. | Refaktor fungsi `hash_password` dan `verify_password` menggunakan API native `bcrypt.hashpw` dan `bcrypt.checkpw`. | Hashing kata sandi berjalan stabil, cepat, dan 100% kompatibel dengan Python 3.13. |
| **D.3 Audit OWASP & BOLA** | Pengecekan otorisasi kepemilikan objek pada `GET /predictions/{id}` awalnya mengembalikan HTTP 404 saat bukan pemilik data. | Praktik umum terkadang menyembunyikan eksistensi resource via 404, namun spesifikasi rubrik praktikum mewajibkan eksplisit HTTP 403 Forbidden. | Tambahkan validasi: `if prediction.user_id != current_user_id: raise HTTPException(status_code=403, detail="Akses ditolak (BOLA Protection)")`. | Status respons HTTP 403 Forbidden lolos pengujian OWASP otomatis dan rubrik praktikum. |

---

## 3. Verifikasi Asumsi Teknis & Keputusan Desain [ASUMSI-XX]

| Kode Asumsi | Isi Asumsi / Keputusan Desain AI | Status Verifikasi Tim | Rasional & Justifikasi Teknis |
| :---: | :--- | :---: | :--- |
| **ASUMSI-01** | Metode autentikasi pengguna menggunakan pasangan kredensial Email dan Password berbasis JWT stateless. | **Diterapkan** | Sesuai kontrak `openapi.yaml` dan memungkinkan skalabilitas horizontal backend tanpa penyimpanan *state* sesi di memori server. |
| **ASUMSI-02** | Fitur inferensi AI menerima masukan berbasis JSON payload (*lag features* penjualan bulanan suku cadang). | **Diterapkan** | Memudahkan integrasi sistem internal bengkel/web client tanpa overhead transfer berkas biner berukuran besar pada inferensi harian. |
| **ASUMSI-03** | Riwayat prediksi dikembalikan dalam bentuk daftar terpaginasi (*limit* default 10, offset 0). | **Diterapkan** | Mencegah ancaman OWASP API4 (*Unrestricted Resource Consumption*) saat jumlah catatan prediksi pengguna bertambah ribuan baris. |
| **ASUMSI-04** | Menggunakan database SQLite untuk lingkungan pengujian lokal dan PostgreSQL untuk lingkungan produksi melalui variabel `DATABASE_URL`. | **Diterapkan** | Menjamin portabilitas penuh bagi penguji tanpa memerlukan instalasi server PostgreSQL terpisah, namun tetap siap produksi via kontainer. |
| **ASUMSI-05** | Penanganan kegagalan model AI menggunakan mekanisme fallback otomatis (*Moving Average*) dengan penanda `is_fallback_triggered = true`. | **Diterapkan** | Menjaga ketersediaan layanan (*high availability*) bengkel otomotif sehingga sistem tetap memberikan rekomendasi stok meski model mengalami anomali. |

---

## 4. Deklarasi Penggunaan & Etika AI

Seluruh interaksi dan kode yang dihasilkan AI telah ditelaah, diaudit secara mandiri terhadap standar keamanan OWASP API Top 10, serta divalidasi menggunakan rangkaian tes unit otomatis Pytest (10 tes lulus 100%). Tidak ada informasi rahasia atau kredensial produksi nyata yang dibagikan selama sesi interaksi AI.
