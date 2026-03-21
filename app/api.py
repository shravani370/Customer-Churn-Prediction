from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("../models/model.pkl")

@app.get("/")
def home():
    return {"message": "Churn Prediction API"}

@app.post("/predict")
def predict(tenure: int, monthly_charges: float, total_charges: float):
    data = np.array([tenure, monthly_charges, total_charges]).reshape(1, -1)

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    return {
        "prediction": int(prediction),
        "churn_probability": float(probability)
    }