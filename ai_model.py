import math
import requests


class MedicalLogisticRegression:
    def __init__(self):
        self.diseases_knowledge = {}
        self.load_knowledge_from_csharp()

    def load_knowledge_from_csharp(self):
        print("Đang tải dữ liệu y khoa từ kho Web nâng cao...")
        try:
            csharp_api_url = "http://localhost:5297/api/Web/AiKnowledge"

            response = requests.get(csharp_api_url)

            if response.status_code == 200:
                data = response.json()
                for item in data:
                    self.diseases_knowledge[item['diseaseName']] = {
                        "bias": -2.0,
                        "weights": {int(k): float(v) for k, v in item['weights'].items()},
                        "desc": item['description'],
                        "treatment": item['treatment']
                    }
                print(f"-> HOÀN TẤT! Đã nạp thành công {len(self.diseases_knowledge)} bệnh lý từ kho Web!")
            else:
                print(f"-> LỖI {response.status_code}: Không thể lấy dữ liệu. Chi tiết: {response.text}")
        except Exception as e:
            print(f"-> LỖI KẾT NỐI: {e}")

    def _sigmoid(self, z):
        z = max(min(z, 250), -250)
        return 1 / (1 + math.exp(-z))

    def predict(self, symptom_ids):
        results = []

        # Logic bóc tách ID nâng cao (chống sập khi nhận Object từ C#)
        normalized_ids = []
        for s in symptom_ids:
            if isinstance(s, dict):
                sym_id = s.get("symptomId", s.get("symptomid"))
                if sym_id is not None: normalized_ids.append(int(sym_id))
            else:
                try:
                    normalized_ids.append(int(s))
                except:
                    pass

        for disease_name, data in self.diseases_knowledge.items():
            z = data["bias"]
            for sym_id in normalized_ids:
                if sym_id in data["weights"]:
                    z += data["weights"][sym_id]

            probability = self._sigmoid(z)

            if probability > 0.01:
                results.append({
                    "diseaseName": disease_name,
                    "probability": round(probability * 100, 1),
                    "description": data["desc"],
                    "treatment": data["treatment"]
                })

        results.sort(key=lambda x: x["probability"], reverse=True)
        return results