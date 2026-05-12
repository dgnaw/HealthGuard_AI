import math
import requests

class MedicalLogisticRegression:
    def __init__(self):
        self.diseases_knowledge = {}
        self.load_knowledge_from_csharp()

    def load_knowledge_from_csharp(self):
        print("Đang tải dữ liệu y khoa từ C# Database...")
        try:
            # LƯU Ý QUAN TRỌNG: Đổi cổng 5245 thành cổng localhost mà Backend C# của bạn đang chạy
            csharp_api_url = "http://localhost:5297/api/Mobile/AiKnowledge"

            response = requests.get(csharp_api_url)

            if response.status_code == 200:
                data = response.json()
                for item in data:
                    self.diseases_knowledge[item['diseaseName']] = {
                        "bias": -2.0,  # Đặt mức Bias mặc định chung cho các bệnh
                        # Đổi lại Key thành kiểu số nguyên (int) cho mảng weights
                        "weights": {int(k): float(v) for k, v in item['weights'].items()},
                        "desc": item['description'],
                        "treatment": item['treatment']
                    }
                print(f"-> HOÀN TẤT! Đã nạp thành công {len(self.diseases_knowledge)} bệnh lý vào AI!")
            else:
                print(f"-> LỖI {response.status_code}: Không thể lấy dữ liệu. Chi tiết từ C#: {response.text}")
        except Exception as e:
            print(f"-> LỖI KẾT NỐI: {e}")

    def _sigmoid(self, z):
        z = max(min(z, 250), -250)
        return 1 / (1 + math.exp(-z))

    def predict(self, symptom_ids):
        results = []

        for disease_name, data in self.diseases_knowledge.items():
            z = data["bias"]

            for sym_id in symptom_ids:
                if sym_id in data["weights"]:
                    z += data["weights"][sym_id]

            probability = self._sigmoid(z)

            # Chỉ trả về những bệnh có tỷ lệ > 1% cho nhẹ máy
            if probability > 0.01:
                results.append({
                    "diseaseName": disease_name,
                    "probability": round(probability * 100, 1),
                    "description": data["desc"],
                    "treatment": data["treatment"]
                })

        # Sắp xếp bệnh tỷ lệ cao lên đầu
        results.sort(key=lambda x: x["probability"], reverse=True)
        return results