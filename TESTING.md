# Dokumentasi Pengujian Sistem (System Testing Documentation)
**Projek:** AI Computer Hardware Image Classification System

## Tujuan Pengujian
Dokumen ini disediakan khusus untuk merekod dan menilai ketepatan model AI (Teachable Machine) serta kestabilan antaramuka (UI) Sistem Klasifikasi Perkakasan Komputer. Pengujian **wajib** menggunakan set imej baharu yang belum pernah didedahkan atau digunakan semasa fasa latihan model (training phase) untuk mengelakkan *overfitting bias* selari dengan standard keperluan Final Assessment (FA).

---

## Senarai Semak Pengujian (Testing Checklist)

Sila tandakan `[ ]` kepada `[x]` apabila pengujian telah selesai dijalankan.

### A. Pengujian Klasifikasi Imej (Image Classification)
Pastikan model diuji menggunakan imej baharu (bukan dari dataset latihan) bagi setiap kelas berikut:
- [ ] Keyboard
- [ ] Mouse
- [ ] RAM
- [ ] HDD
- [ ] Router

### B. Pengujian Kaedah Input (Input Method)
Pastikan kedua-dua saluran data imej berfungsi secara *end-to-end* sehingga ramalan dipaparkan:
- [ ] Muat Naik Imej (Upload image - JPG, PNG, WEBP)
- [ ] Tangkapan Kamera Langsung (Webcam capture)

### C. Pengujian Variasi Suasana (Variation)
Ketahanan model (Model Robustness) diuji dengan mempelbagaikan kondisi imej:
- [ ] Berbeza sudut (Contoh: pandangan atas, pandangan sisi)
- [ ] Berbeza jarak (Dekat/Close-up, Jauh)
- [ ] Berbeza pencahayaan (Terang, Malap/Gelap)
- [ ] Berbeza latar belakang (Background serabut, background putih)
- [ ] Berbeza saiz objek dalam bingkai

### D. Pengujian Pengendalian Ralat (Error Testing & Edge Cases)
Sistem diuji untuk memastikan kegagalan tidak mengakibatkan aplikasi terhenti/rosak secara mendadak (No hard crashes):
- [ ] Objek tidak dikenali (Sengaja tunjukkan cawan/botol)
- [ ] Tahap keyakinan rendah (< 60% confidence -> "Unknown")
- [ ] Imej tidak sah (Muat naik fail PDF, TXT, dll)
- [ ] Akses kamera ditolak oleh pengguna (Camera permission denied)
- [ ] Pelayan (FastAPI) tidak dapat dihubungi (Server offline)
- [ ] Model atau fail Label gagal dijumpai di dalam folder `model/`

---

## Log Keputusan Pengujian (Test Results Log)

*Sila isikan ruangan kosong di bawah berdasarkan keputusan ujian sebenar. Tiada data palsu dibenarkan.*

| Test ID | Actual Class (Sebenar) | Input Method | Prediction (Ramalan) | Confidence (%) | Correct/Incorrect | Remarks (Catatan / Isu / Ralat) |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **IMG-01** | Keyboard | | | | | |
| **IMG-02** | Keyboard | | | | | |
| **IMG-03** | Mouse | | | | | |
| **IMG-04** | Mouse | | | | | |
| **IMG-05** | RAM | | | | | |
| **IMG-06** | RAM | | | | | |
| **IMG-07** | HDD | | | | | |
| **IMG-08** | HDD | | | | | |
| **IMG-09** | Router | | | | | |
| **IMG-10** | Router | | | | | |
| **VAR-01** | [Uji Sudut Berbeza] | | | | | |
| **VAR-02** | [Uji Gelap/Malap] | | | | | |
| **ERR-01** | *Bukan Perkakasan* | | | | | Menguji jika model berani claim (Low confidence) |
| **ERR-02** | *Tiada Imej* | Upload | - | - | - | Muat naik fail PDF, rekod mesej ralat. |
| **ERR-03** | *Camera Denied* | Webcam | - | - | - | Rekod mesej di paparan. |

---
**Pengesahan Penguji:**

Tandatangan: ________________________
Tarikh: ________________________
