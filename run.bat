@echo off
echo ===================================================
echo Memulakan Sistem AI Computer Hardware Classification
echo ===================================================

:: Semak jika folder venv wujud
IF NOT EXIST "venv" (
    echo [1/3] Mencipta 'virtual environment' menggunakan Python 3.12...
    py -3.12 -m venv venv
) ELSE (
    echo [1/3] 'Virtual environment' sudah wujud.
)

:: Aktifkan venv
echo [2/3] Mengaktifkan 'virtual environment'...
call venv\Scripts\activate

:: Pasang keperluan
echo [3/3] Memastikan semua pakej (termasuk TensorFlow) dipasang...
pip install -r requirements.txt

:: Jalankan aplikasi
echo ===================================================
echo Sistem sedia! Memulakan pelayan (Server)...
echo Sila buka pelayar web di: http://127.0.0.1:8000
echo ===================================================
uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
