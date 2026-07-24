from pathlib import Path
import pickle

import numpy as np
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Final_Stroke_Prediction.sav"

with MODEL_PATH.open("rb") as model_file:
    model = pickle.load(model_file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    age = float(request.form["age"])
    bp = 1 if request.form.get("bp", "No").strip().lower() in {"yes", "y", "1", "true"} else 0
    hrd = 1 if request.form.get("hrd", "No").strip().lower() in {"yes", "y", "1", "true"} else 0
    glu = float(request.form["glu"])

    input_df = pd.DataFrame(
        np.array([[age, bp, hrd, glu]], dtype=float),
        columns=["age", "hypertension", "heart_disease", "avg_glucose_level"],
    )
    prediction = int(model.predict(input_df)[0])

    if prediction == 1:
        result = "The risk of getting stroke is high."
    else:
        result = "No stroke risk was detected from the provided information."

    return render_template("result.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
