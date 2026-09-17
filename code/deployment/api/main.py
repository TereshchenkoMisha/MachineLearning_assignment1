import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import MODEL_PATH, FEATURES

app = FastAPI(title="Spotify Genre Prediction API")

if not os.path.exists(MODEL_PATH):
    model = None
else:
    model = joblib.load(MODEL_PATH)

class SongFeatures(BaseModel):
    danceability: float
    energy: float
    valence: float
    tempo: float
    acousticness: float
    loudness: float
    speechiness: float
    instrumentalness: float

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/predict")
def predict_genre(features: SongFeatures):
    global model
    if not model:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=500, detail="Model file not found")
            
    input_dict = features.model_dump() if hasattr(features, "model_dump") else features.dict()
    input_data = pd.DataFrame([input_dict], columns=FEATURES)
    
    prediction = model.predict(input_data)[0]
    return {"prediction": str(prediction)}