from flask import Flask, request, jsonify
import json
from ai_model import MedicalLogisticRegression

app = Flask(__name__)

model = MedicalLogisticRegression()

# Load config (Nhớ thêm encoding='utf-8' để chống lỗi font)
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


@app.route('/predict', methods=['POST'])
def predict_disease():
    try:
        data = request.get_json()

        selected_symptoms = data.get('selectedSymptoms', [])

        if not selected_symptoms:
            return jsonify({"error": "Không có triệu chứng nào được cung cấp."}), 400

        symptom_ids = [item.get('symptomId') for item in selected_symptoms]

        diagnoses = model.predict(symptom_ids)

        return jsonify({
            "status": "Success",
            "diagnoses": diagnoses
        }), 200,

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'], debug=True)