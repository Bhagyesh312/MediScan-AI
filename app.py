from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__, static_folder="static", template_folder="templates")

# Load the pipeline from local path
PIPELINE_PATH = os.path.join(os.path.dirname(__file__), "final_pipeline.pkl")

pipeline = joblib.load(PIPELINE_PATH)
model = pipeline["model"]
label_encoder = pipeline["label_encoder"]
symptom_cols = pipeline["symptom_columns"]

@app.route("/")
def index():
    # Pass symptom list to the template
    return render_template("index.html", symptom_cols=symptom_cols)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        selected_symptoms = data.get("symptoms", [])

        input_vector = np.zeros(len(symptom_cols), dtype=int)
        col_index = {sym: idx for idx, sym in enumerate(symptom_cols)}
        for s in selected_symptoms:
            if s in col_index:
                input_vector[col_index[s]] = 1

        pred_encoded = model.predict(input_vector.reshape(1, -1))[0]
        predicted_disease = label_encoder.inverse_transform([pred_encoded])[0]

        return jsonify({
            "success": True,
            "predicted_disease": str(predicted_disease)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
