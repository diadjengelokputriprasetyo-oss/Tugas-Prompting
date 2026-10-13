# AutoPartSmart — Intelligent Mobile and Web Application Development (IMWAD)

Repositori pengerjaan tugas dan praktikum mata kuliah **Intelligent Mobile and Web Application Development (IMWAD)**.
* **Topik Pertemuan 06:** Implementasi Backend API, Validasi Masukan, Autentikasi JWT, dan Keamanan OWASP API.
* **Dosen Pengampu:** Edwin Hari Agus Prastyo, S.Kom., M.Kom.

---

## 📌 Deliverable PTM-06 Lengkap

| File / Artefak | Lokasi Berkas | Keterangan |
| :--- | :--- | :--- |
| **Source Code Backend Modular** | `backend/app/` | Arsitektur 3-lapisan (Router $\rightarrow$ Service $\rightarrow$ Repository) menggunakan FastAPI & SQLAlchemy. |
| **Environment Template** | `.env.example` & `backend/.env.example` | Template variabel lingkungan aman tanpa hardcoded secrets. |
| **Postman Collection** | `docs/postman/postman-collection.json` | Koleksi request uji Postman v2.1.0 lengkap untuk skenario happy path (200/201) dan error path (400/401/403/404/422). |
| **Laporan Audit OWASP** | `docs/security/owasp-audit.md` | Laporan audit keamanan OWASP API Security Top 10 (2023) beserta kode patch Anti-BOLA dan sanitasi AI. |
| **Log Interaksi Prompt AI** | `docs/prompt-log/ptm-06-prompt-log.md` | Dokumentasi log prompt, evaluasi kualitas, iterasi, dan verifikasi asumsi teknis [ASUMSI-01 s.d. 05]. |
| **Lembar Kerja Praktikum** | `docs/LKP-PTM-06.md` | Dokumen LKP-PTM-06 terisi lengkap mencakup Bagian E dan Bagian F. |

---

## ⚡ Menjalankan Backend Secara Lokal

```bash
# 1. Pemasangan dependensi
pip install -r backend/requirements.txt

# 2. Setup berkas environment
cp .env.example .env

# 3. Jalankan server FastAPI
uvicorn app.main:app --app-dir backend --reload --port 8000
```

Buka dokumentasi OpenAPI interaktif pada browser:
* Swagger UI: `http://localhost:8000/api/v1/docs`

---

## 🧪 Eksekusi Pengujian Otomatis

```bash
pytest backend/tests/ -v
```
Seluruh 10 unit test lulus 100%, memvalidasi alur auth token pair, isolasi data pengguna, proteksi celah BOLA (HTTP 403 Forbidden), dan sanitasi prompt injection model AI.
