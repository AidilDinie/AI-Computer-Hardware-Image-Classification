# --- Import modul yang diperlukan ---
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from PIL import Image, ImageOps
import numpy as np
import io
import os
import uvicorn
import logging

# [Komen: Compatibility Fix]
# Model Teachable Machine (keras_model.h5) dieksport menggunakan format Keras 2 lama.
# TensorFlow versi baru (2.16+) guna Keras 3 secara default, yang tidak serasi
# dengan struktur model lama ini (ralat 'groups' pada DepthwiseConv2D & nested Sequential).
# Baris ini WAJIB diletak SEBELUM 'import tensorflow' supaya TF guna Keras 2 legacy
# (memerlukan pakej 'tf-keras' turut dipasang - lihat requirements.txt).
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# [Komen: Model Loading] Import modul TensorFlow/Keras
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_TERSEDIA = True
except ImportError:
    TF_TERSEDIA = False
    logging.warning("TensorFlow tidak dipasang. Sila pasang dengan 'pip install tensorflow'.")

# --- Inisialisasi aplikasi FastAPI ---
app = FastAPI(
    title="AI Computer Hardware Classification System",
    description="Sistem pengkelasan perkakasan komputer menggunakan FastAPI.",
    version="1.0"
)

# --- Sambungkan laluan /static ke folder static untuk akses CSS & JS ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pembolehubah global untuk menyimpan model dan label
MODEL_AI = None
SENARAI_KELAS = []

# Lokasi fail model
folder_model = "model"
laluan_model = os.path.join(folder_model, "keras_model.h5")
laluan_label = os.path.join(folder_model, "labels.txt")

# --- Kitaran Hayat (Lifespan): Fungsi dijalankan ketika aplikasi dimulakan ---
@app.on_event("startup")
async def muatkan_model_ketika_mula():
    """
    1 & 2. [Komen: Model Loading & Labels] 
    Fungsi ini akan cuba memuatkan model (keras_model.h5) 
    dan senarai label (labels.txt) apabila aplikasi FastAPI dihidupkan.
    """
    global MODEL_AI, SENARAI_KELAS
    
    if not os.path.exists(folder_model):
        os.makedirs(folder_model)
        print(f"Folder '{folder_model}' dicipta. Sila masukkan model ke dalam folder ini.")
        return

    # A. Muatkan model (keras_model.h5)
    if os.path.exists(laluan_model) and TF_TERSEDIA:
        try:
            print(f"Memuatkan model dari {laluan_model}...")
            # Parameter compile=False digunakan kerana kita hanya mahu membuat inference (ramalan), bukan untuk melatih semula model.
            MODEL_AI = load_model(laluan_model, compile=False)
            print("Model AI berjaya dimuatkan!")
        except Exception as e:
            print(f"RALAT: Gagal memuatkan model. {str(e)}")
            MODEL_AI = None
    else:
        if not TF_TERSEDIA:
            print("PENTING: Pakej TensorFlow tidak ditemui. Model tidak dapat dimuatkan.")
        else:
            print(f"PENTING: Fail model tidak wujud di {laluan_model}.")

    # B. Muatkan label (labels.txt)
    if os.path.exists(laluan_label):
        try:
            with open(laluan_label, "r", encoding="utf-8") as fail:
                # 3. [Komen: Labels] Baca fail baris demi baris, dan buang ruang kosong/newline
                kandungan = fail.readlines()
                # Teachable machine format label biasanya "0 Keyboard", jadi kita asingkan nombor.
                SENARAI_KELAS = []
                for baris in kandungan:
                    # Buang nombor indeks jika wujud (contoh "0 Keyboard" menjadi "Keyboard")
                    nama_kelas = baris.strip()
                    if " " in nama_kelas and nama_kelas.split(" ")[0].isdigit():
                        nama_kelas = " ".join(nama_kelas.split(" ")[1:])
                    SENARAI_KELAS.append(nama_kelas)
            print(f"Label berjaya dimuatkan: {SENARAI_KELAS}")
        except Exception as e:
            print(f"RALAT: Gagal membaca fail label. {str(e)}")
            SENARAI_KELAS = []
    else:
        print(f"PENTING: Fail label tidak wujud di {laluan_label}.")

# --- Endpoint GET / : Paparkan Halaman Utama ---
@app.get("/", response_class=HTMLResponse)
async def paparkan_halaman_utama():
    laluan_fail = os.path.join("static", "index.html")
    if os.path.exists(laluan_fail):
        with open(laluan_fail, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse(content="<h1>Ralat: fail index.html Tidak Dijumpai</h1>", status_code=404)


# --- Pydantic Model untuk Response ---
class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    status: str

# --- Endpoint POST /predict : Klasifikasi Imej ---
@app.post("/predict", response_model=PredictionResponse)
async def klasifikasi_imej(file: UploadFile = File(...)):
    """
    Endpoint untuk menerima imej, membuat pra-pemprosesan, dan memulangkan hasil 
    ramalan dari model Google Teachable Machine.
    """
    try:
        # Semak jika sistem gagal memuatkan model atau label semasa startup
        if MODEL_AI is None:
            return JSONResponse(
                content={
                    "prediction": "Tiada Model",
                    "confidence": 0.0,
                    "status": "Model 'keras_model.h5' belum wujud atau gagal dimuatkan."
                }
            )
            
        if len(SENARAI_KELAS) == 0:
            return JSONResponse(
                content={
                    "prediction": "Tiada Label",
                    "confidence": 0.0,
                    "status": "Fail 'labels.txt' tiada atau ralat."
                }
            )

        # 1. Validate fail
        jenis_imej_dibenarkan = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in jenis_imej_dibenarkan:
            return JSONResponse(
                status_code=400,
                content={"status": "Sila muat naik fail imej (JPG, PNG, WEBP)."}
            )
        
        # 2. Baca imej
        kandungan_imej = await file.read()
        imej = Image.open(io.BytesIO(kandungan_imej))
        
        # [Komen: Preprocessing] 
        # Model Teachable Machine memerlukan imej berformat RGB dan bersaiz 224x224.
        if imej.mode != "RGB":
            imej = imej.convert("RGB")
            
        # Kadangkala gambar perlu fit center tanpa stretch, ImageOps.fit membantu (pilihan).
        # Tapi resize asas adalah (224, 224)
        imej = ImageOps.fit(imej, (224, 224), Image.Resampling.LANCZOS)
        
        # Tukarkan imej kepada NumPy array
        imej_array = np.array(imej, dtype=np.float32)
        
        # Normalisasi mengikut format Teachable Machine Keras:
        # Menukar nilai piksel dari (0-255) kepada (-1.0 hingga 1.0)
        imej_array = (imej_array / 127.5) - 1.0
        
        # Tambahkan batch dimension: (224, 224, 3) menjadi (1, 224, 224, 3)
        data_input = np.expand_dims(imej_array, axis=0)
        
        # [Komen: model.predict()]
        # 7. Masukkan data_input ke dalam model untuk mendapatkan ramalan.
        # Fungsi ini akan memulangkan array kebarangkalian bagi setiap kelas.
        ramalan = MODEL_AI.predict(data_input)
        
        # [Komen: Probability]
        # ramalan[0] menyimpan senarai markah (kebarangkalian) untuk setiap kelas.
        # Contoh bentuk: [0.01, 0.98, 0.005, 0.002, 0.003]
        probabilities = ramalan[0]
        
        # [Komen: argmax]
        # 8. Gunakan numpy.argmax untuk mencari indeks array yang mempunyai nilai tertinggi (kebarangkalian tertinggi).
        indeks_tertinggi = np.argmax(probabilities)
        
        # Semak jika indeks tertinggi tidak melebihi bilangan label (elak index out of bound)
        if indeks_tertinggi >= len(SENARAI_KELAS):
            raise ValueError("Model memulangkan kelas melebihi jumlah label di dalam labels.txt.")
            
        # 9. Dapatkan nama kelas (class label) daripada fail label (bukan hardcoded)
        kelas_diramal = SENARAI_KELAS[indeks_tertinggi]
        
        # [Komen: Confidence Score]
        # 10. Kira markah keyakinan (peratusan model percaya jawapan tersebut betul)
        skor_keyakinan = float(probabilities[indeks_tertinggi])
        
        # [Komen: Threshold Keyakinan]
        # Tetapkan had minimum keyakinan (threshold). 
        # Jika model kurang dari tahap ini, kita anggap ia 'Unknown'.
        # Ini penting supaya model tidak memberi jawapan palsu jika ia tidak pasti.
        CONFIDENCE_THRESHOLD = 0.60
        
        # Jika nilai confidence rendah (kurang dari 60%)
        if skor_keyakinan < CONFIDENCE_THRESHOLD:
            return PredictionResponse(
                prediction="Unknown",
                confidence=skor_keyakinan,
                status="Low Confidence"
            )
            
        # Jika berjaya dan keyakinan melepasi threshold
        return PredictionResponse(
            prediction=kelas_diramal,
            confidence=skor_keyakinan,
            status="Classification Successful"
        )
        
    except Exception as ralat:
        return JSONResponse(
            status_code=500,
            content={
                "prediction": "Error",
                "confidence": 0.0,
                "status": f"Ralat: {str(ralat)}"
            }
        )

if __name__ == "__main__":
    print("Memulakan Pelayan...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
