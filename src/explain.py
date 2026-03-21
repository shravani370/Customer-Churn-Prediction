import shap
import joblib
import pandas as pd

model = joblib.load("models/model.pkl")

explainer = shap.Explainer(model)
shap_values = explainer(X)

shap.summary_plot(shap_values, X)