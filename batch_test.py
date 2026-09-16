"""
Batch Testing Script - DKB3263 FA Project
==========================================
Tujuan: Uji SEMUA imej ujian sebenar (bukan dari dataset training) secara automatik
melalui endpoint /predict, kemudian jana:
  1. evidence/04_testing/test_results.json  -> bukti mentah (raw evidence)
  2. TESTING_filled.md                      -> table TESTING.md diisi dgn keputusan SEBENAR

CARA GUNA:
1. Buat folder "test_images/" di root project ini.
2. Dalam "test_images/", buat satu subfolder untuk SETIAP kelas, nama kena SAMA
   PERSIS macam dalam model/labels.txt (tanpa nombor depan):
       test_images/RAM/
       test_images/HARDISK/
       test_images/MOUSE/
       test_images/POWER SUPPLY/
       test_images/KEYBOARD/
3. Letak imej BAHARU (bukan imej yang digunakan semasa training TM) dalam
   setiap subfolder tu. Guna nama fail apa-apa pun boleh (.jpg/.png/.webp).
4. Run:  python batch_test.py
5. Table hasil sebenar akan keluar dalam TESTING_filled.md — copy terus
   masuk TESTING.md, dan JSON dalam evidence/04_testing/ jadi bukti.

PENTING: Script ni TIDAK reka confidence/prediction — semua keputusan
datang terus dari model sebenar yang dimuatkan dalam main.py.
"""
import os
import json
import glob
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

TEST_DIR = "test_images"
EVIDENCE_DIR = "evidence/04_testing"
OUTPUT_JSON = os.path.join(EVIDENCE_DIR, "test_results.json")
OUTPUT_MD = "TESTING_filled.md"


def run_batch_test():
    if not os.path.isdir(TEST_DIR):
        print(f"RALAT: Folder '{TEST_DIR}/' tidak wujud.")
        print("Sila buat folder tu dan letak subfolder ikut nama kelas dalam labels.txt.")
        return

    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    client = TestClient(app)
    results = []

    with client:  # ensures model loads via startup event
        class_folders = sorted(
            d for d in os.listdir(TEST_DIR) if os.path.isdir(os.path.join(TEST_DIR, d))
        )
        if not class_folders:
            print(f"Tiada subfolder kelas dalam '{TEST_DIR}/'. Sila ikut arahan atas skrip ini.")
            return

        counter = 1
        for actual_class in class_folders:
            folder_path = os.path.join(TEST_DIR, actual_class)
            images = sorted(
                glob.glob(os.path.join(folder_path, "*.jpg"))
                + glob.glob(os.path.join(folder_path, "*.jpeg"))
                + glob.glob(os.path.join(folder_path, "*.png"))
                + glob.glob(os.path.join(folder_path, "*.webp"))
            )
            if not images:
                print(f"Amaran: tiada imej dalam {folder_path}, dilangkau.")
                continue

            for img_path in images:
                content_type = "image/jpeg"
                if img_path.lower().endswith(".png"):
                    content_type = "image/png"
                elif img_path.lower().endswith(".webp"):
                    content_type = "image/webp"

                with open(img_path, "rb") as f:
                    response = client.post(
                        "/predict",
                        files={"file": (os.path.basename(img_path), f, content_type)},
                    )

                data = response.json()
                predicted = data.get("prediction", "ERROR")
                confidence = data.get("confidence", 0.0)
                correct = (predicted.strip().upper() == actual_class.strip().upper())

                test_id = f"IMG-{counter:02d}"
                counter += 1

                result_row = {
                    "test_id": test_id,
                    "actual_class": actual_class,
                    "image_file": os.path.basename(img_path),
                    "status_code": response.status_code,
                    "prediction": predicted,
                    "confidence": round(confidence * 100, 2),
                    "correct": correct,
                    "raw_status": data.get("status", ""),
                }
                results.append(result_row)
                mark = "BETUL" if correct else "SALAH"
                print(f"[{test_id}] {actual_class:15s} -> {predicted:15s} "
                      f"({confidence*100:.1f}%)  [{mark}]")

    # --- Save raw JSON evidence ---
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "total_tests": len(results),
        "correct": sum(1 for r in results if r["correct"]),
        "results": results,
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    print(f"\nBukti mentah disimpan: {OUTPUT_JSON}")

    # --- Generate filled markdown table ---
    if results:
        accuracy = 100 * summary["correct"] / summary["total_tests"]
    else:
        accuracy = 0.0

    lines = [
        "# Log Keputusan Pengujian (Auto-Generated dari batch_test.py)",
        "",
        f"Dijana pada: {summary['generated_at']}",
        f"Jumlah ujian: {summary['total_tests']} | Betul: {summary['correct']} | "
        f"Ketepatan keseluruhan: {accuracy:.1f}%",
        "",
        "| Test ID | Actual Class | Fail Imej | Prediction | Confidence (%) | Correct/Incorrect |",
        "| :---: | :--- | :--- | :--- | :---: | :---: |",
    ]
    for r in results:
        status = "Correct" if r["correct"] else "Incorrect"
        lines.append(
            f"| {r['test_id']} | {r['actual_class']} | {r['image_file']} | "
            f"{r['prediction']} | {r['confidence']} | {status} |"
        )
    lines.append("")
    lines.append("> Copy table di atas ke dalam TESTING.md (ganti table kosong asal). "
                  "Semua nilai di atas dari inference SEBENAR, bukan rekaan.")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Table siap: {OUTPUT_MD} (copy masuk TESTING.md)")


if __name__ == "__main__":
    run_batch_test()
