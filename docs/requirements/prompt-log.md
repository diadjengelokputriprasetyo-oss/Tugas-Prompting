# Prompt Log & AI Iteration Documentation - AutoPartSmart

**Nama Produk:** AutoPartSmart (Sistem Peramalan Permintaan & Optimasi Persediaan Suku Cadang Otomotif)  
**Versi Dokumen:** 1.0  
**Tanggal:** 19 September 2026  
**Tim Penyusun:** Product Manager, Requirements Analyst, Agile Product Owner, System Analyst, QA Engineer  

---

## 1. Pendahuluan

Dokumen ini mencatat seluruh *prompt* yang dikirimkan ke AI selama siklus perancangan rekayasa kebutuhan (*requirements engineering*), draf awal jawaban yang dihasilkan oleh AI, serta evaluasi/koreksi manual yang dilakukan oleh tim untuk memastikan kepatuhan terhadap standar ISO/IEC 25010, metodologi Agile, dan fakta hasil riset pada studi kasus.

---

## 2. Tahap 1: Penyusunan Product Requirement Document (PRD)

### 2.1 Prompt Log PRD
* **Peran Prompt:** Senior Product Manager  
* **Tujuan:** Mengubah dokumen riset/kasus persediaan suku cadang otomotif menjadi Draf PRD ringkas terstruktur.  
* **Teks Prompt:**
  ```text
  [Peran] Kamu adalah product manager senior untuk produk Mobile/Web berfitur AI.
  [Tugas] Susun DRAF PRD ringkas untuk "AutoPartSmart" berdasarkan kasus berikut.
  [Konteks]
  Problem statement : Pengelola bengkel kesulitan memprediksi permintaan suku cadang sporadis.
  Target user : Manager Persediaan Bengkel (Pak Budi) & Staf Gudang.
  Platform & stack : Website (React.js, Python FastAPI, PostgreSQL).
  Fitur AI inti : Peramalan Permintaan Suku Cadang Bulanan (KNN & Hybrid SVM-KNN).
  Konstrain : Prototype 1 semester; data & biaya AI terbatas.
  [Format output] Ringkasan eksekutif, Problem statement (fakta vs asumsi), Target user, Value proposition, Tujuan & KPI, Scope MoSCoW, Non-goals, Asumsi & risiko + mitigasi.
