document.addEventListener('DOMContentLoaded', () => {
    // Rujukan elemen DOM
    const btnStartCamera = document.getElementById('btn-start-camera');
    const btnCapture = document.getElementById('btn-capture');
    const imageUpload = document.getElementById('image-upload');
    const btnReset = document.getElementById('btn-reset');
    
    const cameraContainer = document.getElementById('camera-container');
    const webcam = document.getElementById('webcam');
    
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const canvas = document.getElementById('canvas');
    const emptyMessage = document.getElementById('empty-message');
    
    const statusMessage = document.getElementById('status-message');
    const errorMessage = document.getElementById('errorMessage');
    const loadingState = document.getElementById('loading-state');
    const predictionResult = document.getElementById('prediction-result');
    const classNameDisplay = document.getElementById('class-name');
    const confidenceFill = document.getElementById('confidence-fill');
    const confidenceScore = document.getElementById('confidence-score');
    
    let stream = null;
    let currentImageBlob = null;
    let isDetecting = false;
    
    // Kelas perkakasan yang disokong (untuk simulasi)
    const hardwareClasses = ['Keyboard', 'Mouse', 'RAM', 'HDD', 'Router'];

    // 1. Fungsi untuk mulakan kamera web
    btnStartCamera.addEventListener('click', async () => {
        try {
            // Minta akses kamera
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            webcam.srcObject = stream;
            
            // Paparkan antaramuka kamera
            cameraContainer.classList.remove('hidden');
            
            // Mulakan proses auto-detect
            isDetecting = true;
            autoPredictLoop();
            
            // Sembunyikan amaran ralat jika ada
            hideError();
        } catch (err) {
            console.error("Ralat mengakses kamera:", err);
            showError("Tidak dapat mengakses kamera. Sila pastikan anda memberi kebenaran atau guna fungsi muat naik.");
        }
    });

    // 2. Auto Predict Loop (Kamera akan tangkap gambar dan detect secara automatik)
    async function autoPredictLoop() {
        if (!isDetecting || !stream) return;
        
        if (webcam.videoWidth > 0 && webcam.videoHeight > 0) {
            // OPTIMISASI KELAJUAN: Model hanya perlu saiz 224x224.
            // Kita potong (crop) tengah dan saizkan ke 300x300 supaya fail jadi sangat kecil dan laju.
            const targetSize = 300;
            const minDim = Math.min(webcam.videoWidth, webcam.videoHeight);
            const startX = (webcam.videoWidth - minDim) / 2;
            const startY = (webcam.videoHeight - minDim) / 2;
            
            canvas.width = targetSize;
            canvas.height = targetSize;
            
            // Lukis frame video semasa (crop petak tengah) ke dalam canvas
            const ctx = canvas.getContext('2d');
            ctx.drawImage(webcam, startX, startY, minDim, minDim, 0, 0, targetSize, targetSize);
            
            // Tunjuk frame semasa di panel kanan supaya pengguna nampak
            displayPreview(canvas.toDataURL('image/jpeg', 0.8)); // Guna kualiti 80% untuk ringankan lagi
            
            // Tukar canvas kepada Blob (saiz sangat kecil sekarang) untuk dihantar ke server
            canvas.toBlob(async (blob) => {
                if (blob && isDetecting) {
                    const formData = new FormData();
                    formData.append('file', blob, 'image.jpg');
                    
                    try {
                        const response = await fetch('/predict', {
                            method: 'POST',
                            body: formData
                        });
                        
                        if (response.ok) {
                            const data = await response.json();
                            // Jika tiada error, semak markah keyakinan (confidence)
                            if (data.prediction !== "Tiada Model" && data.prediction !== "Error") {
                                // TAPISAN KETEPATAN: Hanya tunjuk jika AI lebih 60% pasti
                                // Ini menghalang tulisan dari 'lompat-lompat' antara mouse dan keyboard
                                if (data.confidence > 0.60) {
                                    displayResult(data);
                                } else {
                                    // Jika kurang pasti, suruh pengguna dekatkan / fokuskan
                                    classNameDisplay.textContent = "Menganalisis... (Fokuskan Imej)";
                                    confidenceScore.textContent = (data.confidence * 100).toFixed(1) + "%";
                                    confidenceFill.style.width = "0%";
                                }
                            }
                        }
                    } catch (err) {
                        console.error("Ralat auto-detect:", err);
                    }
                }
                
                // Teruskan loop dengan lebih laju (300ms) kerana fail dah kecil
                if (isDetecting) {
                    setTimeout(autoPredictLoop, 300);
                }
            }, 'image/jpeg');
        } else {
            // Jika video belum ready, tunggu sekejap dan cuba lagi
            setTimeout(autoPredictLoop, 200);
        }
    }

    // 3. Fungsi untuk muat naik imej dari peranti
    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            // Tutup kamera jika sedang berjalan
            stopCamera();
            
            currentImageBlob = file;
            
            // Gunakan FileReader untuk baca fail dan paparkan pratonton
            const reader = new FileReader();
            reader.onload = (e) => {
                displayPreview(e.target.result);
                processImageForPrediction();
            };
            reader.readAsDataURL(file);
        }
    });

    // 4. Fungsi butang Reset
    btnReset.addEventListener('click', () => {
        resetUI();
    });

    // Fungsi utiliti untuk paparkan pratonton imej
    function displayPreview(src) {
        imagePreview.src = src;
        imagePreview.classList.remove('hidden');
        emptyMessage.classList.add('hidden');
        previewContainer.classList.remove('empty-state');
        btnReset.classList.remove('hidden');
    }

    // Fungsi utiliti untuk hentikan stream kamera
    function stopCamera() {
        isDetecting = false; // Hentikan auto-detect
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        cameraContainer.classList.add('hidden');
        btnCapture.classList.add('hidden');
    }

    // 5. Fungsi utama untuk hantar imej ke endpoint /predict
    async function processImageForPrediction() {
        if (!currentImageBlob) return;
        
        // Sediakan antaramuka UI untuk keadaan "loading"
        hideStatus();
        hideError();
        predictionResult.classList.add('hidden');
        loadingState.classList.remove('hidden');
        
        // Sediakan FormData untuk penghantaran
        const formData = new FormData();
        formData.append('file', currentImageBlob, 'image.jpg');
        
        try {
            // [Komen: Fetch API] Menghantar imej sebenar ke pelayan FastAPI menggunakan POST dan FormData
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            // Dapatkan response JSON daripada pelayan
            const data = await response.json();
            
            // Semak ralat HTTP seperti imej tidak sah (400) atau server ralat (500)
            if (!response.ok) {
                throw new Error(data.status || `Ralat Pelayan: Status HTTP ${response.status}`);
            }
            
            // Semak jika pelayan memulangkan ralat ketiadaan model Google Teachable Machine
            if (data.prediction === "Tiada Model" || data.prediction === "Tiada Label" || data.prediction === "Error") {
                showError(`Ralat AI: ${data.status}`);
                loadingState.classList.add('hidden');
                return;
            }
            
            // Kemaskini UI dengan keputusan sebenar (bukan rekaan/fake)
            displayResult(data);
            
        } catch (error) {
            console.error("Ralat klasifikasi:", error);
            showError(error.message || "Ralat semasa menyambung ke pelayan AI. Pastikan pelayan sedang berjalan.");
            loadingState.classList.add('hidden');
        }
    }

    // 6. Fungsi untuk paparkan keputusan sebenar kepada pengguna
    function displayResult(data) {
        loadingState.classList.add('hidden');
        
        // Tetapkan nama kelas (prediction)
        classNameDisplay.textContent = data.prediction;
        
        // Tukar markah keyakinan dari 0-1 kepada peratusan (contoh: 0.942 -> 94.2%)
        const confPercentage = (data.confidence * 100).toFixed(1);
        confidenceScore.textContent = `${confPercentage}%`;
        
        // Animasikan bar kemajuan (progress bar)
        setTimeout(() => {
            // Gunakan parseFloat untuk style.width bagi mengelakkan pepijat jika ada
            confidenceFill.style.width = `${parseFloat(confPercentage)}%`;
        }, 100);
        
        // Tunjukkan kad keputusan
        predictionResult.classList.remove('hidden');
        
        // Paparkan status keputusan (status mesej dari backend)
        showStatus(data.status);
    }

    // Fungsi utiliti antaramuka
    function showStatus(msg) {
        statusMessage.textContent = msg;
        statusMessage.classList.remove('hidden');
    }

    function hideStatus() {
        statusMessage.classList.add('hidden');
    }

    function showError(msg) {
        const errorEl = document.getElementById('error-message');
        errorEl.textContent = msg;
        errorEl.classList.remove('hidden');
    }

    function hideError() {
        const errorEl = document.getElementById('error-message');
        errorEl.classList.add('hidden');
    }

    function resetUI() {
        stopCamera();
        currentImageBlob = null;
        imageUpload.value = '';
        
        // Reset pratonton
        imagePreview.src = '';
        imagePreview.classList.add('hidden');
        emptyMessage.classList.remove('hidden');
        previewContainer.classList.add('empty-state');
        
        // Reset keputusan dan status
        loadingState.classList.add('hidden');
        predictionResult.classList.add('hidden');
        confidenceFill.style.width = '0%';
        btnReset.classList.add('hidden');
        hideStatus();
        hideError();
    }
});
