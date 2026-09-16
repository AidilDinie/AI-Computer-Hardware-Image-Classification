import os
import json
import io
from PIL import Image
from fastapi.testclient import TestClient
from main import app

def run_test():
    print("Memulakan ujian inference...")
    
    # Create evidence directory if it doesn't exist
    os.makedirs("evidence/07_fastapi", exist_ok=True)
    
    # Create a test client
    client = TestClient(app)
    
    # The 'with client:' block ensures startup events are run (so model loads)
    with client:
        # Create a dummy image
        img = Image.new('RGB', (224, 224), color = 'blue')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Send a POST request to /predict
        print("Menghantar request ke /predict...")
        response = client.post(
            "/predict",
            files={"file": ("test_image.jpg", img_byte_arr, "image/jpeg")}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
        
        # Save output to evidence folder
        evidence_file = "evidence/07_fastapi/inference_output.json"
        with open(evidence_file, "w") as f:
            json.dump({
                "status_code": response.status_code,
                "response": response.json()
            }, f, indent=4)
        print(f"Output ujian telah disimpan ke {evidence_file}")

if __name__ == "__main__":
    run_test()
