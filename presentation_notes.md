# Nota Pembentangan Projek & Penjelasan Kod
**Projek:** AI Computer Hardware Image Classification System

Dokumen ini disediakan khas sebagai skrip rujukan pantas semasa pembentangan individu (Presentation) anda. Ia menerangkan setiap baris kod kritikal dengan format yang ringkas, mudah difahami, dan terus kepada tujuan (straight to the point).

---

## BAHAGIAN A: PYTHON (FastAPI Backend)

### 1. `FastAPI`
- **Fungsi:** Kerangka kerja (framework) utama untuk membina pelayan web (server).
- **Kenapa digunakan:** Ia sangat laju, moden, dan sesuai untuk menerima permintaan (request) imej daripada pengguna secara berterusan.
- **Jika dibuang:** Pelayan web backend tidak akan wujud, dan keseluruhan sistem terhenti.
- **Ayat Pembentangan:** *"Saya menggunakan FastAPI sebagai tunjang utama backend kerana ia sangat laju dan cekap mengendalikan permintaan berbanding framework lama."*

### 2. `UploadFile` dan `File`
- **Fungsi:** Syntax khas FastAPI untuk menangkap dan menerima fail yang dimuat naik (dalam kes ini, gambar perkakasan).
- **Kenapa digunakan:** Fail imej bukan sekadar teks biasa. Ia perlukan kaedah ini untuk dibaca dalam bentuk *bytes* dan disimpan di dalam memori sementara (RAM).
- **Jika dibuang:** Backend kita akan buta; ia tidak dapat menerima gambar dari frontend.
- **Ayat Pembentangan:** *"Modul UploadFile membolehkan sistem menerima gambar yang dihantar dari kamera atau storan pengguna secara terus ke memori, tanpa perlu disimpan (save) dalam hard disk."*

### 3. `Pillow (Image.open)`
- **Fungsi:** Sebuah pustaka (library) pemprosesan imej untuk membuka dan mengolah fail gambar.
- **Kenapa digunakan:** Gambar perlu diubah saiz (resize) kepada 224x224 piksel dan ditukar warnanya ke RGB supaya menepati format AI kita.
- **Jika dibuang:** Imej tidak dapat dibuka atau saiznya salah, menyebabkan AI menolak gambar tersebut.
- **Ayat Pembentangan:** *"Pillow digunakan sebagai pra-pemprosesan untuk memastikan setiap gambar dipotong dan diseragamkan saiznya sebelum diimbas oleh AI."*

### 4. `NumPy (np.array)`
- **Fungsi:** Menukarkan gambar yang kita nampak kepada deretan nombor (tatasusunan/array).
- **Kenapa digunakan:** Model AI tidak melihat gambar seperti manusia; ia hanya melihat dan mengira nilai matriks nombor.
- **Jika dibuang:** Model AI tidak dapat membaca gambar tersebut (kerana masih berformat piksel imej).
- **Ayat Pembentangan:** *"NumPy bertindak menterjemah gambar fizikal tersebut menjadi data angka supaya otak AI boleh melakukan pengiraan matematik."*

### 5. `TensorFlow / load_model`
- **Fungsi:** Memuatkan otak AI (model `keras_model.h5`) ke dalam sistem.
- **Kenapa digunakan:** Ini adalah enjin utama yang membawa segala memori latihan dari Google Teachable Machine ke dalam pelayan tempatan (local server) kita.
- **Jika dibuang:** Kita tidak mempunyai AI, cuma aplikasi biasa.
- **Ayat Pembentangan:** *"Saya menggunakan pustaka TensorFlow untuk mengekstrak dan menghidupkan model Keras yang telah dilatih, membolehkannya bekerja secara offline tanpa internet."*

### 6. `Preprocessing` (e.g. `(imej_array / 127.5) - 1.0`)
- **Fungsi:** Menyelaras nilai warna dari 0-255 menjadi skala negatif ke positif (-1 hingga 1).
- **Kenapa digunakan:** Ini adalah syarat wajib (requirement) bagi mana-mana model yang dihasilkan dari platform Google Teachable Machine.
- **Jika dibuang:** Keputusan ramalan AI akan menjadi cacat dan salah 100%.
- **Ayat Pembentangan:** *"Saya melakukan prapemprosesan atau Normalization untuk meratakan tahap pencahayaan gambar supaya model tidak keliru dengan pantulan cahaya yang melampau."*

### 7. `model.predict()`
- **Fungsi:** Menghantar imej (yang sudah ditukar ke nombor tadi) masuk ke dalam lapisan (layers) AI untuk mendapatkan tekaan.
- **Kenapa digunakan:** Di sinilah keajaiban berlaku, proses yang dipanggil *Inference* bermula.
- **Jika dibuang:** Tiada sebarang ramalan dilakukan.
- **Ayat Pembentangan:** *"Fungsi predict() adalah detik di mana AI memproses imej tersebut di dalam *neural network* dan memulangkan markah markah kebarangkalian (probabilities) bagi setiap komponen."*

### 8. `np.argmax()`
- **Fungsi:** Mencari kedudukan indeks (nombor) yang mempunyai markah (score) tertinggi.
- **Kenapa digunakan:** AI mengembalikan markah seperti `[0.01, 0.94, 0.02...]`. Argmax akan mencari markah tertinggi (`0.94`) dan memberitahu kita bahawa ia berada di posisi ke-2 (Mouse).
- **Jika dibuang:** Kita terpaksa membaca senarai nombor markah satu persatu menggunakan loop yang membebankan pelayan.
- **Ayat Pembentangan:** *"Bagi menentukan jawapan akhir, np.argmax digunakan bagi memilih kelas perkakasan yang mendapat peratusan undian tertinggi dari senarai AI."*

### 9. `Confidence Score` & Threshold
- **Fungsi:** Tahap peratusan seberapa yakin AI terhadap jawapannya. 
- **Kenapa digunakan:** (Threshold) Jika AI kurang dari 60% yakin, ia akan disekat dan diisytiharkan sebagai "Unknown".
- **Jika dibuang:** AI akan berteka secara membabi buta walaupun ia sekadar ditunjukkan gambar sebuah cawan.
- **Ayat Pembentangan:** *"Sistem ini dipasangkan penapis keyakinan atau threshold. Jika AI ragu-ragu di bawah 60%, ia akan memulangkan ralat berbanding berbohong."*

### 10. `JSONResponse`
- **Fungsi:** Membungkus hasil ramalan ke dalam format JSON (`{"prediction": "Mouse", "confidence": 0.94}`).
- **Kenapa digunakan:** Format bahasa sejagat yang difahami oleh Javascript pada Frontend.
- **Jika dibuang:** Frontend dan Backend gagal berkomunikasi.
- **Ayat Pembentangan:** *"Keputusan akhirnya dibungkus kemas dalam bentuk JSON supaya antaramuka Javascript mudah menterjemahnya menjadi bentuk visual."*

---

## BAHAGIAN B: JAVASCRIPT (Web UI Frontend)

### 1. `DOM Manipulation (getElementById)`
- **Fungsi:** Kod Javascript "menangkap" butang, gambar, dan teks yang berada pada skrin (HTML).
- **Kenapa digunakan:** Supaya kita boleh menyembunyikan/menunjukkan sesuatu, atau menukar teks keputusan secara dinamik (real-time).
- **Jika dibuang:** UI akan kaku/statik dan tidak bertindak balas apabila butang ditekan.
- **Ayat Pembentangan:** *"Semua pengurusan pergerakan aplikasi dan butang dikawal oleh DOM Manipulation bagi mewujudkan susunan kad yang saling berinteraksi."*

### 2. `Event Listener (click/change)`
- **Fungsi:** "Mendengar" jika pengguna sedang mengeklik butang atau memuat naik fail.
- **Kenapa digunakan:** Kita perlukan kod untuk "bangun" dan berkerja hanya apabila pengguna melakukan sesuatu tindakan.
- **Jika dibuang:** Tindakan tekan butang tidak membuahkan sebarang hasil.
- **Ayat Pembentangan:** *"Event listener membolehkan aplikasi saya menunggu arahan pengguna sebelum menggerakkan kamera atau memulakan pengimbasan AI."*

### 3. `getUserMedia()` & `Webcam`
- **Fungsi:** Meminta akses terus kepada perkakasan kamera komputer/telefon bimbit pengguna.
- **Kenapa digunakan:** Mewujudkan pengalaman pengecaman perkakasan masa nyata (*real-time inspection*).
- **Jika dibuang:** Sistem hanya bergantung pada muat naik gambar manual semata-mata.
- **Ayat Pembentangan:** *"Dengan menggunakan kaedah getUserMedia, sistem ini bersifat responsif membenarkan lensa peranti pengguna menjadi mata kepada model AI secara langsung."*

### 4. `Canvas (.drawImage)`
- **Fungsi:** "Membekukan" (freeze) video kamera yang bergerak menjadi satu gambar statik (snapshot).
- **Kenapa digunakan:** Model AI tidak boleh membaca video terus, ia hanya membaca imej (frame tunggal).
- **Jika dibuang:** Gambar dari webcam gagal ditangkap/disalin untuk diuji.
- **Ayat Pembentangan:** *"Walaupun kita memaparkan video hidup, teknik disebalik tabir menggunakan canvas untuk menangkap satu bingkai *frame* lalu menghantarnya kepada AI."*

### 5. `FormData`
- **Fungsi:** Membungkus fail gambar seperti bungkusan surat (parcel) di Pejabat Pos untuk dihantar ke server.
- **Kenapa digunakan:** Imej mempunyai bait data yang besar, tidak boleh dihantar melalui URL biasa.
- **Jika dibuang:** Gambar gagal dipindahkan dari pelayar pengguna ke pelayan FastAPI.
- **Ayat Pembentangan:** *"Pakej FormData digunakan agar penghantaran fail imej yang berat kekal selamat dan utuh sewaktu melalui rangkaian internet ke backend."*

### 6. `fetch()` dan `async/await`
- **Fungsi:** Pekerja pos yang membawa `FormData` ke pelayan, dan menunggu sehingga pelayan memberikan bungkusan jawapan (JSON).
- **Kenapa digunakan:** `async/await` memastikan skrin tidak "freeze" (sangkut) sementara menunggu AI di pelayan selesai berfikir.
- **Jika dibuang:** Tiada perhubungan antara aplikasi pengguna dan AI di belakang tabir.
- **Ayat Pembentangan:** *"Proses fetch API dengan asynchronous ini sangat penting kerana ia membenarkan animasi pemuatan (loading) terus bergerak lancar sementara AI saya giat memproses gambar."*

---

## BAHAGIAN C: DOKUMENTASI BUKTI (AI CODE ASSISTANT)
*Ini adalah cadangan huraian yang boleh digunakan untuk menyiapkan bahagian "Evidence 09" anda di dalam penilaian akhir FA, membuktikan anda mengaplikasikan AI dalam pembangunan sistem.*

### Bukti 1: Peringkat Debugging / Error Fixing
* **Senario Realiti:** Anda menghadapi masalah (*error*) di mana gambar yang diambil melalui webcam tidak boleh terus dibaca oleh FastAPI kerana ia berbentuk Blob, bukan UploadFile biasa. Terdapat ralat jenis "Invalid Format" atau HTTP 400.
* **Tindakan AI Assistant:** Anda memberikan (prompt) keseluruhan `script.js` dan ralat HTTP 400 tersebut kepada AI. AI Assistant membantu menyelesaikan ralat dengan menyarankan penggunaan `canvas.toBlob()` yang kemudiannya dimampatkan (append) ke dalam `FormData('file', blob, 'image.jpg')`.
* **Sebab Digunakan:** Mengurangkan masa memburu ralat perbezaan format fail antara Javascript dan endpoint Pydantic FastAPI.

### Bukti 2: Peringkat Code Generation / Improvement (Polishing UI)
* **Senario Realiti:** Anda mempunyai borang input HTML biasa dan butang yang kaku. Anda ingin membina satu aplikasi gred-profesional bertemakan "Futuristic AI" tanpa membazir masa berminggu-minggu mencipta animasi *loading* dari sifar.
* **Tindakan AI Assistant:** Anda memohon bantuan AI (prompt) untuk *"Polish UI kepada Glassmorphism, tambah kesan glow pada progress bar, dan masukkan animasi loading menggunakan SVG/CSS"*. AI menjana blok CSS moden sepenuhnya (CSS variables, backdrop-filter, keyframes animation) sambil mengekalkan logik backend anda dengan selamat.
* **Sebab Digunakan:** Meningkatkan nilai estetika dan User Experience (UX) projek akademik ke tahap yang sangat profesional dengan efisien. 
*(Anda boleh screenshot paparan chat di mana saya menukar CSS anda sebentar tadi sebagai bukti mutlak)*.
