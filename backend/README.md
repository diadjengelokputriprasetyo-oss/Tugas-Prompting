# AutoPartSmart Backend Service (PTM-06)

Layanan backend API berbasis **FastAPI** dengan arsitektur modular 3-lapisan (*Router* $\rightarrow$ *Service* $\rightarrow$ *Repository*), autentikasi JWT stateless (Access + Refresh Token), proteksi terhadap celah keamanan **OWASP API Security Top 10 (2023)**, serta inferensi model peramalan suku cadang otomotif AI AutoPartSmart.

---

## 📁 Struktur Direktori Modular

```text
backend/
├── app/
│   ├── core/                  # Konfigurasi, Database Engine, Keamanan JWT & Sanitizer
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── sanitizer.py
│   │   └── security.py
│   ├── models/                # SQLAlchemy ORM Models (Users & Predictions)
│   │   ├── prediction.py
│   │   └── user.py
│   ├── repositories/          # Lapisan Query Database Terisolasi
│   │   ├── prediction_repository.py
│   │   └── user_repository.py
│   ├── routers/               # Lapisan HTTP Routing / Controllers
│   │   ├── auth.py
│   │   ├── predictions.py
│   │   └── users.py
│   ├── schemas/               # Skema Validasi Pydantic v2
│   │   ├── common.py
│   │   ├── prediction.py
│   │   ├── token.py
│   │   └── user.py
│   ├── services/              # Logika Bisnis & Inferensi AI ML
│   │   ├── ai_service.py
│   │   ├── auth_service.py
│   │   └── prediction_service.py
│   └── main.py                # Entrypoint FastAPI & Middleware
├── tests/                     # Rangkaian Tes Otomatis Pytest
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_owasp_bola.py
│   └── test_predictions.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Panduan Menjalankan Layanan

### 1. Prasyarat Lingkungan
* Python 3.10+ (Diuji pada Python 3.13)
* Virtual Environment aktif

### 2. Pemasangan Dependensi
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Environment Variable
Salin berkas template lingkungan:
```bash
cp .env.example .env
```

### 4. Menjalankan Server Pengembangan
```bash
uvicorn app.main:app --reload --port 8000
```
Server akan aktif pada:
* URL Utama: `http://localhost:8000`
* Dokumentasi Interaktif Swagger UI: `http://localhost:8000/api/v1/docs`
* Dokumentasi ReDoc: `http://localhost:8000/api/v1/redoc`

---

## 🧪 Menjalankan Rangkaian Pengujian Otomatis

Jalankan pengujian unit dan verifikasi OWASP Anti-BOLA menggunakan Pytest:
```bash
pytest tests/ -v
```
Seluruh 10 tes mencakup alur registrasi, login bcrypt, pasangan token JWT, proteksi BOLA/IDOR (HTTP 403), serta sanitasi prompt injection AI.

---

## 🛡️ Fitur Keamanan OWASP API Top 10 (2023)
* **Anti-BOLA (API1:2023):** Verifikasi kepemilikan objek pada seluruh query dan detail resource berparameter ID.
* **Autentikasi Stateless (API2:2023):** Hashing bcrypt cost 12, token pair (Access Token 30 menit & Refresh Token 7 hari).
* **Sanitasi Masukan AI:** Validasi string anti Prompt Injection dan pembatasan berkas unggah ($\le 5\text{MB}$, MIME whitelisting).
* **Anti Resource Exhaustion (API4:2023):** Paginasi query aman dengan batas maksimum limit.
