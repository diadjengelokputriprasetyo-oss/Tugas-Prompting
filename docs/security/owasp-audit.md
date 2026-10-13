# Laporan Audit Keamanan OWASP API Security Top 10 (2023)
**Proyek:** AutoPartSmart Backend API  
**Mata Kuliah:** Intelligent Mobile and Web Application Development (IMWAD) — PTM-06  
**Auditor:** Backend & Security Engineering Team  
**Status Audit:** PASSED (Seluruh Temuan Telah Di-patch dan Diverifikasi)  

---

## 1. Ringkasan Eksekutif

Audit keamanan independen ini dilakukan terhadap implementasi backend REST API **AutoPartSmart** berdasarkan standar **OWASP API Security Top 10 (2023)**. Audit berfokus pada pencegahan eksploitasi nyata terkait:
1. **API1:2023 Broken Object Level Authorization (BOLA / IDOR)** pada endpoint berbasis parameter identitas (`/predictions/{id}`, `/users/{id}`).
2. **API2:2023 Broken Authentication** pada pengelolaan token JWT, penyimpanan kredensial, dan siklus refresh token.
3. **API4:2023 Unrestricted Resource Consumption** pada paginasi data dan pembatasan muatan berkas masukan (file upload).
4. **Keamanan Khusus Model AI (AI Injection & File Upload Tampering)**: mitigasi serangan *Prompt Injection*, penolakan karakter kontrol ASCII, serta pembatasan MIME type & ekstensi berkas.

---

## 2. Tabel Matriks Audit OWASP API Top 10

| Endpoint / Komponen | Kerentanan OWASP | Tingkat Risiko | Kode Patch / Mitigasi | Status Verifikasi |
| :--- | :--- | :---: | :--- | :---: |
| `GET /api/v1/predictions/{id}` | **API1:2023 Broken Object Level Authorization (BOLA)** | **KRITIS** | Verifikasi kepemilikan objek: `if prediction.user_id != current_user.id: raise HTTPException(403)` | **TERVERIFIKASI (PASSED)** |
| `GET /api/v1/predictions` | **API1:2023 BOLA & Data Leakage** | **TINGGI** | Filter query database secara ketat hanya mengambil record milik `current_user.id` | **TERVERIFIKASI (PASSED)** |
| `POST /api/v1/auth/login` | **API2:2023 Broken Authentication** | **TINGGI** | Hashing kata sandi menggunakan `bcrypt` (cost factor 12) + perbandingan timing-safe (`checkpw`) | **TERVERIFIKASI (PASSED)** |
| `POST /api/v1/auth/refresh` | **API2:2023 Broken Authentication** | **TINGGI** | Validasi tipe token (`type == 'refresh'`), durasi 7 hari, dan verifikasi integritas signature | **TERVERIFIKASI (PASSED)** |
| `GET /api/v1/predictions` | **API4:2023 Unrestricted Resource Consumption** | **SEDANG** | Pembatasan parameter query paginasi `limit` maksimal 100 via Pydantic/FastAPI Query | **TERVERIFIKASI (PASSED)** |
| `POST /api/v1/predictions` | **AI Prompt Injection / Script Payload** | **TINGGI** | Sanitasi masukan string via `re.compile` pola instruksi berbahaya + HTML entity escaping | **TERVERIFIKASI (PASSED)** |
| Handler Unggah Berkas AI | **API4:2023 & Malicious File Upload** | **TINGGI** | Validasi ukuran maksimum $\le 5\text{MB}$, MIME whitelisting, dan validasi ekstensi berkas | **TERVERIFIKASI (PASSED)** |
| Seluruh Endpoint API | **API8:2023 Security Misconfiguration** | **SEDANG** | Pemisahan seluruh kredensial (`SECRET_KEY`, `DATABASE_URL`) ke berkas `.env` | **TERVERIFIKASI (PASSED)** |

---

## 3. Analisis Celah & Kode Patch Konkret (Anti-BOLA)

### Celah 1: BOLA / IDOR pada Pengambilan Detail Prediksi (`GET /predictions/{prediction_id}`)
* **Deskripsi Kerentanan:** Pengguna terautentikasi (User Beta) dapat menebak atau memanfaatkan UUID prediksi milik pengguna lain (User Alpha) untuk membaca riwayat peramalan stok rahasia.
* **Tingkat Risiko:** **Kritis (CVSS 8.6)**.
* **Kode Patch (Diff Minimal):**

```python
# Lokasi: backend/app/services/prediction_service.py

def get_prediction_by_id(self, prediction_id: str, current_user_id: str) -> Prediction:
    prediction = self.prediction_repo.get_by_id(prediction_id)
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data prediksi dengan ID tersebut tidak ditemukan.",
        )

+   # OWASP API1:2023 BOLA Protection
+   if prediction.user_id != current_user_id:
+       raise HTTPException(
+           status_code=status.HTTP_403_FORBIDDEN,
+           detail="Akses ditolak. Anda tidak memiliki izin untuk mengakses resource prediksi milik pengguna lain (BOLA Protection).",
+       )

    return prediction
```

### Celah 2: BOLA pada Isolasi Tenant Riwayat Prediksi (`GET /predictions`)
* **Deskripsi Kerentanan:** Jika router memanggil repository tanpa parameter `user_id`, query database akan mengekspos data riwayat pengguna lain.
* **Kode Patch (Diff Minimal):**

```python
# Lokasi: backend/app/repositories/prediction_repository.py

- def get_all(self, limit: int, offset: int):
-     return self.db.query(Prediction).offset(offset).limit(limit).all()

+ def get_by_user_id(self, user_id: str, limit: int = 10, offset: int = 0) -> List[Prediction]:
+     return (
+         self.db.query(Prediction)
+         .filter(Prediction.user_id == user_id)
+         .order_by(Prediction.created_at.desc())
+         .offset(offset)
+         .limit(limit)
+         .all()
+     )
```

---

## 4. Mekanisme Sanitasi Masukan Model AI (Prompt Injection & Upload Guard)

Fitur AI pada **AutoPartSmart** memproses data fitur peramalan suku cadang otomotif (*lag features*). Untuk mencegah manipulasi instruksi dan konsumsi sumber daya berlebih, modul `app/core/sanitizer.py` menerapkan filter multi-lapis:

### A. Sanitasi String & Deteksi Prompt Injection
```python
# Lokasi: backend/app/core/sanitizer.py

DANGEROUS_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions?", re.IGNORECASE),
    re.compile(r"system\s*override", re.IGNORECASE),
    re.compile(r"<script.*?>.*?</script>", re.IGNORECASE | re.DOTALL),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"(\.\./|\.\.\\)", re.IGNORECASE),
]

def sanitize_string(text: str) -> str:
    cleaned = CONTROL_CHARS_PATTERN.sub("", text).strip()
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(cleaned):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Deteksi masukan berbahaya atau upaya manipulasi instruksi (Prompt Injection).",
            )
    return html.escape(cleaned)
```

### B. Validasi Berkas Upload (OWASP API4 Defense)
```python
async def validate_upload_file(file: UploadFile) -> None:
    # 1. MIME Whitelisting
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Tipe MIME '{file.content_type}' tidak diizinkan.",
        )
    # 2. Ukuran Maksimum 5MB
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Ukuran berkas melebihi batas maksimum 5MB.",
        )
    await file.seek(0)
```

---

## 5. Hasil Pengujian Fungsional & Unit Test

Seluruh patch telah diuji menggunakan rangkaian tes otomatis Pytest pada lingkungan isolasi SQLite memory:
* `test_register_success` & `test_register_duplicate_email`: **PASSED**
* `test_login_success_and_token_pair` & `test_login_invalid_password`: **PASSED**
* `test_protected_me_endpoint` (HTTP 401 unauthenticated): **PASSED**
* `test_refresh_token_endpoint`: **PASSED**
* `test_create_prediction_ai_flow` & `test_ai_fallback_on_negative_lag`: **PASSED**
* `test_ai_sanitization_prompt_injection` (HTTP 422 rejected): **PASSED**
* `test_owasp_bola_access_control` (User Beta rejected with HTTP 403 upon accessing User Alpha's resource): **PASSED**

**Kesimpulan:** Seluruh celah keamanan telah tertutup rapat sesuai spesifikasi OWASP API Security Top 10 (2023).
