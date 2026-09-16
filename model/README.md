# Folder Model AI

Folder ini digunakan untuk menyimpan model AI yang telah dilatih menggunakan **Google Teachable Machine**.

## Fail yang diperlukan

Selepas melatih model di Teachable Machine, eksport model sebagai **TensorFlow (Keras)** dan letakkan fail berikut di sini:

| Fail                | Penerangan                                |
|---------------------|--------------------------------------------|
| `keras_model.h5`    | Fail model Keras (dimuatkan oleh `main.py` melalui `load_model()`) |
| `labels.txt`        | Senarai nama kelas (satu kelas per baris, format `0 NamaKelas`) |

Status semasa: **kedua-dua fail di atas sudah ada dalam folder ini** (5 kelas: RAM, HARDISK, MOUSE, POWER SUPPLY, KEYBOARD).

## Contoh `labels.txt`

```
0 RAM
1 HARDISK
2 MOUSE
3 POWER SUPPLY
4 KEYBOARD
```

## Cara Eksport dari Teachable Machine

1. Buka [Teachable Machine](https://teachablemachine.withgoogle.com/)
2. Latih model dengan imej kelas yang diperlukan
3. Klik **Export Model**
4. Pilih tab **Tensorflow** → **Keras** → **Download my model**
5. Ekstrak `keras_model.h5` dan `labels.txt` ke folder ini

## ⚠️ Nota

- Fail model (`.h5`) tidak disimpan di GitHub kerana saiznya besar (lihat `.gitignore`).
- `main.py` memuatkan model dengan `load_model(..., compile=False)` — hanya untuk inference, bukan untuk latihan semula.
