# LEMBAR KERJA PRAKTIKUM
## Intelligent Mobile and Web Application Development

| Unsur Informasi | Detail Pelaksanaan |
| :--- | :--- |
| **Mata Kuliah** | Intelligent Mobile and Web Application Development |
| **Kode / SKS** | TIF-IMWAD / 3 SKS |
| **Program Studi** | Teknik Informatika |
| **Pertemuan ke-** | 06 dari 16 |
| **Topik** | Implementasi Backend API, Validasi Masukan, Autentikasi JWT, dan Keamanan OWASP API |
| **CPMK** | CPMK-2 → Sub-CPMK 2.1 & 2.2 (Backend Services, Auth JWT & Keamanan OWASP API) |
| **Dosen Pengampu** | Edwin Hari Agus Prastyo, S.Kom., M.Kom. |
| **Durasi** | ±50 menit sesi kelas + Tugas Mandiri Lanjutan |
| **Semester / T.A.** | Ganjil 2025/2026 |

---

### ▌ IDENTITAS MAHASISWA
* **Nama Mahasiswa :** _______________________________________
* **NIM :** _______________________________________
* **Kelompok / Anggota :** Tim Pengembang AutoPartSmart

---

## A. Tujuan Pembelajaran
1. Mengimplementasikan arsitektur backend modular 3 lapisan (Router, Service, Repository) berdasarkan kontrak OpenAPI 3.0 (PTM-05).
2. Membangun sistem autentikasi dan otorisasi stateless berbasis JSON Web Token (JWT) dengan OAuth2 Password Flow, refresh token, dan hashing password bcrypt.
3. Melakukan audit mandiri keamanan API berbasis OWASP API Security Top 10 (2023), menutup celah Broken Object Level Authorization (BOLA), dan menerapkan sanitasi masukan inferensi AI.
4. Melakukan pengujian fungsional API terstruktur menggunakan Postman dan mendokumentasikan Postman Collection yang dapat diimpor ulang.

---

## B. Checklist Bahan Awal
| Status | Bahan Awal |
| :---: | :--- |
| [x] | `openapi.yaml` (PTM-05) — spesifikasi kontrak REST API 3.0 yang telah lolos validasi. |
| [x] | `erd.md` / `models.py` (SQLAlchemy / Pydantic) — skema pemodelan database PTM-05. |
| [x] | Keputusan stack backend: **FastAPI (Python)** dengan arsitektur Router-Service-Repository. |
| [x] | Library autentikasi terpasang: `python-jose[cryptography]`, `bcrypt`, `pydantic-settings`, `python-multipart`. |
| [x] | Akses ke endpoint model AI lokal / script mock inferensi AI AutoPartSmart beserta Postman Collection. |

---

## C. Alur Praktikum Sesi Kelas (±50 Menit)
1. **Review OpenAPI (5 mnt):** Identifikasi endpoint CRUD, Autentikasi (`/auth/*`), dan AI (`/predictions/*`).
2. **Prompt AI Scaffold (15 mnt):** Pembuatan scaffold modular `routers/`, `services/`, `repositories/`, `models/`, `core/`.
3. **Prompt AI Auth JWT (15 mnt):** Implementasi signup/register, login bcrypt, token pair (30 menit & 7 hari), dan `GET /auth/me`.
4. **Prompt AI Audit OWASP (10 mnt):** Penutupan celah BOLA pada `GET /predictions/{id}` (403 Forbidden) dan helper sanitasi Prompt Injection.
5. **Uji Postman & Export (5 mnt):** Pengujian happy path & error path serta ekspor ke `docs/postman/postman-collection.json`.

---

## D. Checklist Hasil Prompt Siap Pakai

### Checklist Scaffold & Modularitas (D.1)
| Status | Indikator |
| :---: | :--- |
| [x] | Struktur direktori backend terpisah tegas: `routers/`, `services/`, `repositories/`, `models/`, `core/`. |
| [x] | Koneksi basis data terkelola dengan session lifecycle yang aman (auto-close via `get_db` generator, `pool_pre_ping=True`, anti connection leak). |
| [x] | File `.env.example` tersedia lengkap di root dan direktori backend dengan placeholder variabel tanpa mengekspos kredensial rahasia riil. |

### Checklist Autentikasi JWT (D.2)
| Status | Indikator |
| :---: | :--- |
| [x] | Kata sandi pengguna di-hash menggunakan bcrypt dengan salt aman sebelum disimpan ke database. |
| [x] | Alur token pair aktif: Access token berdurasi 30 menit dan Refresh token berdurasi 7 hari. |
| [x] | Endpoint `GET /auth/me` terproteksi penuh dan menolak request tanpa `Authorization: Bearer <token>` (HTTP 401). |

### Checklist Keamanan API OWASP (D.3)
| Status | Indikator |
| :---: | :--- |
| [x] | Seluruh endpoint CRUD berparameter ID memiliki verifikasi kepemilikan objek (`resource.user_id == current_user.id`), menolak akses pengguna lain dengan **HTTP 403 Forbidden**. |
| [x] | Endpoint inferensi AI memiliki validasi ketat ukuran berkas upload ($\le 5\text{MB}$) dan whitelisting tipe MIME (`image/jpeg`, `image/png`, `text/csv`). |
| [x] | Input teks fitur AI disanitasi dari karakter kontrol ASCII dan upaya prompt injection berbahaya sebelum diproses oleh model. |

---

## E. Lembar Kerja Isian Mahasiswa

### E.1 Daftar Endpoint Backend & Status Implementasi Lapisan
*Tanda (*) mengindikasikan endpoint berbasis kecerdasan buatan (AI).*

| No | Resource / Endpoint | HTTP Method | Lapisan Terpasang (Router / Svc / Repo) | Status & Cek OWASP Anti-BOLA |
| :---: | :--- | :---: | :--- | :--- |
| 1 | `/api/v1/auth/register` (alias `/signup`) | `POST` | Router (`auth.py`) $\rightarrow$ Service (`auth_service.py`) $\rightarrow$ Repo (`user_repository.py`) | **Aktif**; Password di-hash bcrypt, cek email duplikat (400), validasi input (422). |
| 2 | `/api/v1/auth/login` | `POST` | Router (`auth.py`) $\rightarrow$ Service (`auth_service.py`) $\rightarrow$ Repo (`user_repository.py`) | **Aktif**; Timing-safe password verification, mengembalikan access token (30m) & refresh token (7d). |
| 3 | `/api/v1/auth/refresh` | `POST` | Router (`auth.py`) $\rightarrow$ Service (`auth_service.py`) $\rightarrow$ Repo (`user_repository.py`) | **Aktif**; Validasi signature & expiry refresh token, terbitkan access token baru (401 jika invalid). |
| 4 | `/api/v1/auth/me` | `GET` | Router (`auth.py`) $\rightarrow$ Dependency (`dependencies.py`) $\rightarrow$ Repo (`user_repository.py`) | **Aktif**; Terproteksi Bearer JWT; menolak unauthenticated request dengan status 401. |
| 5 | `*` `/api/v1/predictions` | `POST` | Router (`predictions.py`) $\rightarrow$ Service (`prediction_service.py` & `ai_service.py`) $\rightarrow$ Repo (`prediction_repository.py`) | **Aktif**; Sanitasi input anti prompt injection, SHA-256 hash, inferensi ML/KNN, fallback otomatis. |
| 6 | `/api/v1/predictions` | `GET` | Router (`predictions.py`) $\rightarrow$ Service (`prediction_service.py`) $\rightarrow$ Repo (`prediction_repository.py`) | **Aktif**; **Anti-BOLA**: query terisolasi hanya menampilkan prediksi milik `current_user.id`, paginasi `limit` $\le 100$. |
| 7 | `/api/v1/predictions/{id}` | `GET` | Router (`predictions.py`) $\rightarrow$ Service (`prediction_service.py`) $\rightarrow$ Repo (`prediction_repository.py`) | **Aktif**; **Anti-BOLA**: verifikasi kepemilikan objek (`prediction.user_id == current_user.id`), tolak ID pengguna lain via **HTTP 403 Forbidden**. |
| 8 | `/api/v1/users/{id}` | `GET` | Router (`users.py`) $\rightarrow$ Repo (`user_repository.py`) | **Aktif**; **Anti-BOLA**: pengguna biasa dilarang mengakses ID profil pengguna lain (HTTP 403 Forbidden). |

#### Deskripsi Endpoint Inferensi AI (*) & Mekanisme Validasi/Sanitasi Masukan:
Endpoint `POST /api/v1/predictions` berfungsi melakukan peramalan kebutuhan suku cadang otomotif (*demand forecasting*) dan perhitungan *safety stock* otomatis berdasarkan riwayat permintaan suku cadang (*lag_1*, *lag_2*, *lag_3*).

Mekanisme validasi & sanitasi yang diterapkan:
1. **Sanitasi String & Anti-Prompt Injection (`app/core/sanitizer.py`):** Masukan teks disaring menggunakan ekspresi reguler terhadap pola eksploitasi prompt (seperti `ignore previous instructions`, `system override`, payload skrip HTML/JS). Pelanggaran langsung ditolak dengan status HTTP 422.
2. **Karakter Kontrol ASCII:** Karakter kontrol non-printable dihapus guna mencegah *log injection* dan anomali parser JSON.
3. **Penyandian Input (Input Hash Traceability):** Seluruh masukan kanonikal dihitung nilai SHA-256 hash (`input_hash`) untuk menjamin integritas audit data inferensi.
4. **Mekanisme Fallback Otomatis:** Apabila masukan mengandung nilai anomali (misal lag bernilai negatif) atau kegagalan internal pemrosesan, sistem tidak melakukan *crash*, melainkan secara otomatis mengaktifkan algoritma *Moving Average* konservatif dengan penanda `is_fallback_triggered = true` dan nilai *confidence score* yang disesuaikan (0.65).

---

### E.2 Iterasi & Revisi Prompt AI

| Prompt | Masalah pada Output AI Pertama | Revisi / Prompt Lanjutan yang Digunakan |
| :--- | :--- | :--- |
| **D.1 Scaffold Modular** | Konfigurasi database SQLAlchemy pada SQLite lokal mengalami masalah konkurensi thread saat diakses FastAPI secara paralel. | *Tambahkan parameter `connect_args={'check_same_thread': False}` pada konfigurasi `create_engine` dan pastikan session ditutup dalam blok `finally`.* |
| **D.2 Autentikasi JWT** | Pustaka `passlib` memicu galat `AttributeError: module 'bcrypt' has no attribute '__about__'` pada Python 3.13 karena versi bcrypt 4+. | *Ganti wrapper passlib dengan pemanggilan langsung pustaka native `bcrypt` (`bcrypt.hashpw` dan `bcrypt.checkpw`) yang sepenuhnya kompatibel dengan Python 3.13.* |
| **D.3 Audit OWASP & BOLA** | Endpoint `GET /predictions/{id}` awalnya mengembalikan HTTP 404 ketika pengguna lain mencoba mengakses ID prediksi tersebut. | *Tambahkan verifikasi eksplisit: jika record ditemukan namun `prediction.user_id != current_user.id`, wajib lemparkan `HTTPException(status_code=403, detail='Akses ditolak (BOLA Protection)')`.* |

---

### E.3 Asumsi Teknis & Keputusan Desain Backend [ASUMSI-XX]

| Kode Asumsi | Isi Asumsi / Keputusan Desain AI | Verifikasi Tim (Diterapkan / Diubah / Ditolak) |
| :---: | :--- | :---: |
| **ASUMSI-01** | Autentikasi menggunakan metode stateless berbasis JWT Access Token (durasi 30 menit) dan Refresh Token (durasi 7 hari) menggunakan algoritma HS256. | **Diterapkan** |
| **ASUMSI-02** | Fitur inferensi AI menerima masukan berbasis format JSON yang merepresentasikan fitur lag suku cadang (`item_id`, `lag_1`, `lag_2`, `lag_3`). | **Diterapkan** |
| **ASUMSI-03** | Riwayat prediksi dikembalikan secara terpaginasi dengan batasan `limit` maksimum 100 untuk mencegah konsumsi sumber daya berlebih (OWASP API4). | **Diterapkan** |
| **ASUMSI-04** | Menggunakan UUID string 36-karakter sebagai Primary Key entitas pengguna dan prediksi agar kompatibel lintas basis data (SQLite dan PostgreSQL). | **Diterapkan** |
| **ASUMSI-05** | Mekanisme inferensi dilengkapi *fallback engine* otomatis berbasis rata-rata bergerak saat terjadi anomali masukan numerik. | **Diterapkan** |

---

## F. Log Prompt Wajib (ptm-06-prompt-log)

| No | Target Prompt | Alat AI & Versi | Ringkasan Prompt | Kualitas Output (1-5) | Revisi Manual |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **D.1 Scaffold Modular** | Gemini 3.8 Flash (High) | Membuat scaffold backend modular 3 lapisan (Router $\rightarrow$ Service $\rightarrow$ Repository) sesuai `openapi.yaml`. | **5** | Menyesuaikan model basis data untuk kompatibilitas SQLite/PostgreSQL. |
| **2** | **D.2 Autentikasi JWT** | Gemini 3.8 Flash (High) | Implementasi OAuth2 Password Flow, token pair JWT (30 menit & 7 hari), serta hashing kata sandi bcrypt. | **4** | Refaktor implementasi bcrypt langsung untuk kompatibilitas penuh Python 3.13. |
| **3** | **D.3 Audit OWASP & BOLA** | Gemini 3.8 Flash (High) | Audit celah keamanan OWASP API Top 10, patch BOLA (HTTP 403), dan sanitasi masukan fitur AI. | **5** | Menambahkan regex pattern anti-prompt injection dan batas query paginasi. |
| **4** | **Iterasi Lanjutan** | Gemini 3.8 Flash (High) | Penyesuaian skema Pydantic v2 dan instalasi `email-validator` untuk validasi format surel. | **5** | Migrasi `Config` class menjadi `ConfigDict` dan pembaruan `requirements.txt`. |

---

## G. Deliverable Checklist

| File / Artefak | Lokasi di Repositori | Keterangan | Status |
| :--- | :--- | :--- | :---: |
| Source code backend modular | `backend/app/` | Struktur modular Router, Service, Repository, model, dan handler auth | **Lengkap** |
| `.env.example` | Root & `backend/` | Template environment variable aman tanpa nilai rahasia riil | **Lengkap** |
| `postman-collection.json` | `docs/postman/` | Koleksi request uji API lengkap untuk skenario sukses dan alur error | **Lengkap** |
| `owasp-audit.md` | `docs/security/` | Laporan audit OWASP API Security Top 10 beserta cuplikan kode patch | **Lengkap** |
| `ptm-06-prompt-log.md` | `docs/prompt-log/` | Log prompt + iterasi + evaluasi + verifikasi asumsi (WAJIB) | **Lengkap** |
| LKP-PTM-06 (lembar ini) | `docs/LKP-PTM-06.md` | Lembar kerja praktikum terisi lengkap | **Lengkap** |

---

## H. Bukti Verifikasi Tes Otomatis (Pytest)

Rangkaian 10 pengujian otomatis berhasil dijalankan dengan hasil kelulusan 100%:
```text
backend/tests/test_auth.py::test_register_success PASSED                 [ 10%]
backend/tests/test_auth.py::test_register_duplicate_email PASSED         [ 20%]
backend/tests/test_auth.py::test_login_success_and_token_pair PASSED     [ 30%]
backend/tests/test_auth.py::test_login_invalid_password PASSED           [ 40%]
backend/tests/test_auth.py::test_protected_me_endpoint PASSED            [ 50%]
backend/tests/test_auth.py::test_refresh_token_endpoint PASSED           [ 60%]
backend/tests/test_owasp_bola.py::test_owasp_bola_access_control PASSED  [ 70%]
backend/tests/test_predictions.py::test_create_prediction_ai_flow PASSED [ 80%]
backend/tests/test_predictions.py::test_ai_sanitization_prompt_injection PASSED [ 90%]
backend/tests/test_predictions.py::test_ai_fallback_on_negative_lag PASSED [100%]

======================= 10 passed in 9.21s =======================
```

---
*Praktikum Tugas Mandiri PTM-06 — Intelligent Mobile and Web Application Development*  
*Copyright © Edwin Hari Agus Prastyo, S.Kom., M.Kom.*
