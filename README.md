# AI Computer Hardware Image Classification System

## 1. Project Title
AI Computer Hardware Image Classification System

## 2. Project Description
Sistem pintar berasaskan web yang menggunakan teknologi *Kecerdasan Buatan (AI)* untuk mengecam dan mengklasifikasikan imej perkakasan komputer secara masa nyata (real-time). Ia membolehkan pengguna memuat naik gambar atau menggunakan kamera (webcam) untuk menganalisis perkakasan komputer tanpa memerlukan bantuan pakar.

## 3. Problem Statement
Bagi mereka yang baru mengenali dunia IT atau pelajar komputer, membezakan pelbagai komponen perkakasan (hardware) yang kelihatan rumit boleh menjadi satu cabaran. Tanpa bantuan juruteknik, sukar untuk mengetahui nama komponen tersebut semata-mata dengan melihat bentuk fizikalnya.

## 4. Objectives
- Membangunkan model AI yang mampu mengenali jenis-jenis perkakasan komputer.
- Membina aplikasi web yang interaktif dan mudah digunakan oleh pelbagai lapisan masyarakat.
- Membantu pengguna mengenali komponen IT dengan pantas hanya menggunakan fungsi kamera atau muat naik imej.

## 5. Project Scope
Projek ini difokuskan secara eksklusif kepada pengecaman jenis perkakasan (*Image Classification*) dan bukannya pengesanan kotak kedudukan objek (*Object Detection / Bounding Box*). Aplikasi akan memberikan satu (1) keputusan kelas utama bagi setiap imej yang dimasukkan.

## 6. Target Classes
Sistem ini direka dan dilatih untuk mengecam lima (5) kelas perkakasan komputer berikut:
1. Keyboard (Papan Kekunci)
2. Mouse (Tetikus)
3. RAM (Memori Akses Rawak)
4. HDD (Cakera Keras)
5. Power Supply (Bekalan Kuasa)

## 7. Technologies Used
- **Frontend**: HTML5, CSS3 (Antaramuka *Glassmorphism* Moden), Vanilla JavaScript
- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **AI/ML Base**: Google Teachable Machine, TensorFlow/Keras, NumPy, Pillow

## 8. Google Teachable Machine
Enjin AI di sebalik projek ini dilatih menggunakan [Google Teachable Machine](https://teachablemachine.withgoogle.com/). Platform tersebut membolehkan latihan algoritma Rangkaian Neural (*Neural Network*) secara visual yang pantas, dan model siap boleh dieksport terus ke format `keras_model.h5`.

## 9. Dataset
Dataset imej dihimpun dan dimuat naik ke Google Teachable Machine oleh pengguna. Kualiti dataset amat penting dan perlu merangkumi pelbagai variasi persekitaran bagi memastikan AI dapat membezakan corak perkakasan dengan tepat.

## 10. Model Training
Semasa fasa latihan, AI belajar membezakan corak unik setiap perkakasan (seperti bentuk kunci pada keyboard, cip pada RAM, dan antena pada router). Proses ini menggunakan algoritma prapelatihan (pre-trained model) di latar belakang sistem Google.

## 11. Model Testing
Ujian (*testing*) diwajibkan untuk menggunakan **imej baharu** yang berbeza daripada imej yang dimasukkan semasa latihan (*unseen data*). Langkah ini adalah krusikal untuk memastikan ketepatan model tidak terbias akibat *overfitting*. Butiran ujian ada di `TESTING.md`.

## 12. Experiments
Sekurang-kurangnya dua variasi eksperimen dilaksanakan. Eksperimen membandingkan antara model *Baseline* (latihan asas) dan model *Improved* (latihan dengan peningkatan variasi). Keputusan perbandingan ini diseragamkan di `EXPERIMENTS.md`.

## 13. Application
Aplikasi ini menampilkan susun atur responsif berkonsepkan *Futuristic AI* yang kemas, menampilkan *Glassmorphism panels* (lapisan kaca separa lutsinar) bagi mencapai tahap estetika pameran (demo ready).

## 14. Webcam
Pengguna diberi fungsi membenarkan (allow) akses **Kamera** peranti (*webcam*). Kamera akan dipaparkan secara langsung (*live*) di aplikasi membolehkan tangkapan (*capture*) imej diambil pada bila-bila masa.

## 15. Image Upload
Bagi memudahkan pengesanan imej dari folder simpanan tempatan, satu butang **Muat Naik** (*Upload*) tersedia yang menyokong format standard (.jpg, .png, .webp).

## 16. FastAPI
Digerakkan oleh kerangka **FastAPI** yang ringan dan pantas. Backend ini bertanggungjawab menerima isyarat POST, memproses imej menggunakan NumPy dan Pillow, serta membuat tekaan hasil daripada muatan model Keras.

## 17. Pydantic
Digunakan untuk pengesahan jenis (*type validation*) dalam pengaturcaraan, membolehkan JSON yang masuk dan keluar dikawal ketat formatnya.

## 18. Prediction
Logik AI beroperasi menerusi perintah matematik `np.argmax(probabilities)` bagi mencari nombor indeks (kelas) yang mengandungi markah ramalan yang paling tinggi dalam senarai.

## 19. Confidence Score
Peratusan tahap keyakinan (*confidence*) dikira oleh model dan dipaparkan kepada pengguna (Contoh: 94.2%). Jika keyakinan jatuh di bawah nilai ambang `60%`, sistem tidak akan mencipta keputusan palsu, sebaliknya mengisytiharkan statusnya sebagai **Unknown (Low Confidence)**.

## 20. Project Architecture
1. **Frontend (Klien)** menangkap gambar dari pelayar (browser).
2. Imej dibungkus (FormData) dan di-*POST* menggunakan **Fetch API** ke Endpoint `/predict`.
3. **Backend (FastAPI)** membersihkan, *resize* tepat pada ukuran 224x224, dan menyesuaikan piksel imej kepada susunan tatasusunan (arrays).
4. Data array ini diberi makan (*fed*) kepada model **Keras (.h5)**.
5. Maklumat ramalan dibungkus dalam bentuk JSON dan dipulangkan kepada skrin *Frontend* secara masa nyata.

## 21. Folder Structure
```text
AI-Computer-Hardware-Image-Classification/
├── model/              # (Diperlukan) Folder meletakkan keras_model.h5 dan labels.txt
├── static/             # Fail UI pelayar (index.html, style.css, script.js)
├── evidence/           # Log evidens, tangkapan skrin, dan bukti kerja
├── main.py             # Kod pelayan Python / FastAPI endpoint
├── requirements.txt    # Spesifikasi perpustakaan (library dependencies)
├── .gitignore          # Kawalan halangan muat naik Git (elak pycache/venv)
├── TESTING.md          # Borang pengujian fizikal model
└── EXPERIMENTS.md      # Rekod perbandingan model eksperimen (Baseline vs Improved)
```

## 22. Installation
1. Pastikan peranti dilengkapi dengan pemasangan **Python 3.9+**.
2. Buka aplikasi Terminal / Command Prompt pada komputer anda.
3. *Clone* atau muat turun folder repository ini.
4. (Opsional) Pasang *Virtual Environment*: `python -m venv venv` dan kemudian aktifkannya.
5. Muat turun pakej bergantung (dependencies):
   ```bash
   pip install -r requirements.txt
   ```

## 23. How to Run
Sesudah pemasangan pakej berjaya, jalankan pelayan dengan kod di bawah:
```bash
python main.py
```
Akses URL berikut di aplikasi pelayar Web anda: `http://localhost:8000`

## 24. How to Add Model
Aplikasi ini disediakan **kosong tanpa model terbina**. Untuk mengaktifkan enjin AInya:
1. Pergi ke *Google Teachable Machine* dan buat latihan (train).
2. Tekan kotak *Export Model* dan pilih tab *TensorFlow (Keras)*.
3. Anda akan mendapat muat turun fail berformat `.zip`.
4. Ekstrak, kemudian bawa masuk (copy-paste) fail `keras_model.h5` dan `labels.txt` ke dalam folder `model/` di sistem ini.
5. Mulakan semula pelayan (*Restart Server*).

## 25. Testing
Rujuk pada paparan fail `TESTING.md`. Prosedur ini sangat mustahak bagi membuktikan model dapat mentafsir situasi variasi dunia fizikal tanpa hanya bergantung pada data hafalan.

## 26. Limitations
- Ketepatan sistem sangat rapuh terhadap perubahan persekitaran (Environment Shift) jika data latihan di *Teachable Machine* terlalu seragam (kurang variasi).
- Aplikasi tidak mampu mencari kedudukan lebih dari satu objek pada satu imej. Sekiranya pelbagai perkakasan dihimpunkan, ia mungkin hanya mengecam satu bentuk yang dominan sahaja (tiada *Bounding Box*).

## 27. Future Improvements
- Mengevolusikan model dari *Image Classification* kepada algoritma *Object Detection* yang kompleks seperti YOLOv8. Ia membolehkan pelbagai perkakasan yang diserakkan di atas meja di-"scan" serentak secara masa nyata.
- Menambah sistem Pangkalan Data (Database) untuk menyimpan sejarah imbasan pelajar.
