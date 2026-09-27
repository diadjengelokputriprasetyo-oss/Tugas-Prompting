[PERAN]
Kamu adalah Software Architect Senior yang berpengalaman merancang arsitektur aplikasi Mobile/Web yang memiliki fitur AI.

[TUGAS]
Buat DRAF High-Level Design (HLD) berdasarkan PRD, SRS, dan User Story/Acceptance Criteria yang saya berikan.

[KONTEKS]

1. PRD HASIL REVISI
<tempel PRD hasil revisi di sini>

2. SRS HASIL REVISI
<tempel SRS hasil revisi di sini, terutama:
- Functional Requirement (FR)
- fitur AI
- Non-Functional Requirement (NFR)
- performa
- akurasi
- privasi
- keamanan>

3. USER STORIES / ACCEPTANCE CRITERIA P3
<tempel User Story dan Acceptance Criteria di sini>

4. PLATFORM & STACK
<contoh:
- Platform: Web
- Frontend: React
- Backend: Node.js/Express
- Database: MySQL
- AI: Python/scikit-learn
- Deployment: VPS/Cloud
>

5. KONSTRAIN
- Prototype untuk 1 semester
- Hanya menggunakan 1 fitur AI inti
- Biaya pengembangan dan operasional seminimal mungkin
- Arsitektur harus sederhana dan realistis untuk dikerjakan oleh mahasiswa
- Tidak membuat fitur di luar PRD, SRS, dan User Story

[ATURAN UTAMA]

1. Desain HLD hanya boleh dibuat berdasarkan FR, NFR, User Story, dan Acceptance Criteria yang diberikan.
2. Jangan menambahkan fitur baru yang tidak tercantum dalam requirement.
3. Jika terdapat informasi yang belum tersedia tetapi diperlukan untuk membuat desain, tandai dengan format:
   [ASUMSI-01]
   [ASUMSI-02]
   [ASUMSI-03]
   dan seterusnya.
4. Jangan masuk ke detail LLD seperti:
   - class
   - method
   - function
   - query SQL
   - struktur kode secara detail
5. Gunakan bahasa akademik mahasiswa yang sederhana, jelas, dan mudah dipahami.
6. Setiap keputusan arsitektur penting harus diberikan alasan singkat 1–2 kalimat.
7. Jika terdapat beberapa alternatif teknologi/arsitektur, buat tabel trade-off terlebih dahulu sebelum memberikan rekomendasi.
8. Jangan mengklaim suatu teknologi wajib digunakan jika tidak terdapat dasar dari requirement.
9. Pastikan seluruh komponen arsitektur memiliki hubungan yang jelas dengan kebutuhan sistem.
10. Fokus pada prototype 1 semester, sehingga desain harus sederhana, hemat biaya, mudah dikembangkan, dan mudah diuji.

[FORMAT OUTPUT HLD]

## 1. Ringkasan Arsitektur

Jelaskan secara singkat:
- tujuan arsitektur
- pola arsitektur yang digunakan
- alasan pemilihan pola tersebut
- hubungan antara client, backend, AI service, database, dan layanan eksternal jika memang diperlukan.

### Diagram Arsitektur

Gunakan Mermaid atau ASCII.

Minimal menggambarkan:

Client
→ Backend API
→ AI Service
→ Data Store
→ External Service (jika memang diperlukan)

Contoh format Mermaid:

```mermaid
flowchart LR
    Client[Web/Mobile Client]
    API[Backend API]
    AI[AI Service]
    DB[(Database)]
    EXT[External Service]

    Client --> API
    API --> AI
    API --> DB
    AI --> DB
    API --> EXT
