from fastapi import FastAPI, UploadFile, File, HTTPException
import pefile
import math
import joblib
import pandas as pd
import uvicorn
import os
import sys

# Ensure the parent directory is in the path to module "app" can be resolved
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Malware Classification API", description="Upload a PE file for static analysis and classification")

# Load model, scaler and expected features
model_path = os.path.join(os.path.dirname(__file__), 'model', 'malware_classifier.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), 'model', 'scaler.pkl')
features_path = os.path.join(os.path.dirname(__file__), 'model', 'features.pkl')

if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(features_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    expected_features = joblib.load(features_path)
else:
    print("Warning: Model or scaler not found. Please train the model first.")
    model = None
    scaler = None
    expected_features = None

def extract_features(file_path):
    """Extracts features from a PE file using pefile according to the new dataset structure"""
    try:
        pe = pefile.PE(file_path)
        
        # We need to map pefile properties to these columns:
        # AddressOfEntryPoint, MajorLinkerVersion, MajorImageVersion, MajorOperatingSystemVersion, 
        # DllCharacteristics, SizeOfStackReserve, NumberOfSections, ResourceSize
        
        features = {}
        features['AddressOfEntryPoint'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        features['MajorLinkerVersion'] = pe.OPTIONAL_HEADER.MajorLinkerVersion
        features['MajorImageVersion'] = pe.OPTIONAL_HEADER.MajorImageVersion
        features['MajorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MajorOperatingSystemVersion
        features['DllCharacteristics'] = pe.OPTIONAL_HEADER.DllCharacteristics
        features['SizeOfStackReserve'] = pe.OPTIONAL_HEADER.SizeOfStackReserve
        features['NumberOfSections'] = pe.FILE_HEADER.NumberOfSections
        
        # Calculate roughly ResourceSize
        resource_size = 0
        if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
            for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if hasattr(entry, 'directory'):
                    for res_entry in entry.directory.entries:
                        if hasattr(res_entry, 'directory'):
                            for lang_entry in res_entry.directory.entries:
                                resource_size += lang_entry.data.struct.Size
        features['ResourceSize'] = resource_size
        
        return features
    except Exception as e:
        raise ValueError(f"Failed to parse PE file: {str(e)}")

@app.post("/predict/")
async def predict_malware(file: UploadFile = File(...)):
    if not model or not scaler or not expected_features:
         raise HTTPException(status_code=500, detail="Model not loaded on the server")
         
    if not file.filename.endswith(('.exe', '.dll')):
        raise HTTPException(status_code=400, detail="Only .exe and .dll files are supported")
        
    temp_file = f"temp_{file.filename}"
    try:
        with open(temp_file, "wb") as f:
            f.write(await file.read())
            
        features = extract_features(temp_file)
        
        # Create DataFrame with exact column names and order
        df_features = pd.DataFrame([features])[expected_features]
        scaled_features = scaler.transform(df_features)
        
        prediction = model.predict(scaled_features)[0]
        prediction_prob = model.predict_proba(scaled_features)[0].max() if hasattr(model, "predict_proba") else None
        
        result_label = "Malicious" if prediction == 1 else "Benign"
        
        response = {
            "filename": file.filename,
            "features_extracted": features,
            "prediction": result_label,
            "confidence": f"{prediction_prob*100:.2f}%" if prediction_prob else "N/A"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
    return response

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
