[PERAN]
Kamu adalah Software Engineer Senior yang berpengalaman dalam pengembangan aplikasi sesuai stack teknologi yang digunakan oleh tim.

[TUGAS]
Buat DRAF Low-Level Design (LLD) untuk fitur prioritas MUST pada SRS berdasarkan HLD hasil revisi.

LLD harus cukup detail agar dapat digunakan sebagai acuan implementasi oleh developer, tetapi tetap tidak mengubah requirement yang sudah ditetapkan pada SRS dan HLD.

[KONTEKS]

1. SRS HASIL REVISI
<tempel SRS hasil revisi di sini>

Fokus pada:
- Functional Requirement (FR) berprioritas MUST
- Non-Functional Requirement (NFR) yang terkait dengan fitur MUST
- Fitur AI yang termasuk prioritas MUST

2. HLD HASIL REVISI
<tempel HLD hasil revisi di sini>

Fokus pada:
- Komponen arsitektur
- Modul
- Kontrak API
- Aliran data
- Komponen AI
- Database
- Security & privacy
- Deployment

3. STACK & POLA
Platform:
<contoh: Flutter / Web>

Frontend:
<contoh: Flutter>

Backend:
<contoh: Node.js + Express>

Database:
<contoh: PostgreSQL>

AI:
<contoh: Python + scikit-learn / AI API>

API:
<contoh: REST API>

Architecture Pattern:
<contoh: MVVM / Clean Architecture>

Library/framework lain:
<jika ada, tuliskan>

Jika stack belum ditentukan, tuliskan:
[BELUM DITENTUKAN]

[KONSTRAIN]
- Prototype 1 semester
- Implementasi hanya berdasarkan requirement SRS
- Tidak mengubah FR/NFR
- Fokus pada fitur prioritas MUST
- Fitur AI hanya sesuai yang ditentukan pada SRS/HLD
- Implementasi harus realistis untuk dikerjakan oleh tim mahasiswa
- Biaya seminimal mungkin

==================================================
[ATURAN UTAMA]
==================================================

1. Semua desain LLD WAJIB diturunkan dari SRS dan HLD yang diberikan.

2. DILARANG:
   - menambah requirement baru
   - mengubah requirement
   - menghilangkan requirement
   - membuat fitur tambahan yang tidak ada di SRS/HLD
   - mengasumsikan fitur sebagai requirement resmi

3. Jika terdapat informasi yang belum diputuskan, jangan langsung memilih secara sepihak.

   Berikan:
   - 2 opsi yang memungkinkan
   - kelebihan/kekurangan masing-masing
   - kriteria pemilihan

   Kemudian tuliskan:

   [KEPUTUSAN TIM: ... ]

   Bagian tersebut harus dianggap sebagai keputusan yang masih harus ditentukan oleh tim.

4. Gunakan:
   - Nama class dalam Bahasa Inggris
   - Nama method dalam Bahasa Inggris
   - Nama atribut/field dalam Bahasa Inggris
   - Nama endpoint/API dalam Bahasa Inggris
   - Penjelasan menggunakan Bahasa Indonesia

5. Gunakan penamaan yang konsisten antara:
   - class
   - database
   - API
   - request/response
   - sequence diagram
   - SRS
   - HLD

6. Jangan masuk terlalu jauh ke detail implementasi kode seperti:
   - source code lengkap
   - konfigurasi server lengkap
   - query kompleks yang tidak diperlukan
   - detail deployment infrastructure

7. Namun, desain class, method, database, API, dan sequence harus cukup detail sehingga developer dapat mulai melakukan implementasi.

8. Jika suatu informasi tidak tersedia pada SRS/HLD, tandai:

   [ASUMSI-01]
   [ASUMSI-02]
   [ASUMSI-03]

   Jangan menyamarkan asumsi sebagai requirement.

==================================================
[OUTPUT LLD]
==================================================

# 1. DESAIN MODUL / CLASS

Pilih 2–3 fitur MUST paling penting berdasarkan SRS.

Fitur WAJIB mencakup fitur AI apabila fitur AI merupakan bagian dari prioritas MUST.

Untuk setiap fitur, buat:

## 1.X Nama Fitur

### Tujuan
Jelaskan fungsi fitur berdasarkan FR yang relevan.

### Modul/Class

Buat tabel:

| Class/Module | Layer | Responsibility | Key Attributes | Main Methods |
|---|---|---|---|---|

Contoh layer jika sesuai dengan HLD:
- Presentation
- ViewModel
- Domain
- Use Case
- Repository
- Service
- Controller
- AI Service
- Data Access

Jangan membuat layer yang tidak sesuai dengan pola arsitektur pada HLD.

### Detail Class

Untuk setiap class utama jelaskan:

#### Class: `ClassName`

**Responsibility:**
...

**Attributes:**
- `attributeName`: tipe data — penjelasan
- `attributeName`: tipe data — penjelasan

**Methods:**
- `methodName()`: tujuan method
- `methodName()`: tujuan method

**Dependencies:**
- `ClassName`
- `ClassName`

Jangan menulis source code lengkap.

### Relasi Antar-Class

Gunakan Mermaid UML/class diagram jika memungkinkan.

Contoh:

```mermaid
classDiagram
    class FeatureController {
        +createFeature()
        +getFeature()
    }

    class FeatureService {
        +processFeature()
    }

    class FeatureRepository {
        +save()
        +findById()
    }

    FeatureController --> FeatureService
    FeatureService --> FeatureRepository
