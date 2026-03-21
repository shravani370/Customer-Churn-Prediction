import joblib
import numpy as np

model = joblib.load("models/model.pkl")

def predict(data):
    data = np.array(data).reshape(1, -1)
    result = model.predict(data)
    prob = model.predict_proba(data)

    return result[0], prob[0][1]