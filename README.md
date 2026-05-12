***
## 🤖 AI Chat Sentiment Analysis Service



Đây là một Microservice độc lập chuyên xử lý và phân loại cảm xúc văn bản (Sentiment Analysis) sử dụng thuật toán **Logistic Regression tự viết (From Scratch)**. 

Service này được thiết kế theo chuẩn API RESTful, có thể giao tiếp độc lập với **BẤT KỲ** hệ thống Backend (Java, C#, C++, Node.js...) hay Frontend (React, Vue, Mobile App...) nào thông qua giao thức HTTP.

---

## ⚙️ 1. Cài đặt và Khởi chạy

Yêu cầu hệ thống: Có cài đặt Python 3.x.

**Bước 1:** Cài đặt thư viện bắt buộc
```bash
pip install flask
```

**Bước 2:** Khởi chạy Server AI
```bash
python server.py
```
*Mặc định, server sẽ chạy tại địa chỉ: `http://localhost:5000`*

---

## 🛠 2. Cấu hình hệ thống (config.json)

Bạn không cần sửa code Python để thay đổi cổng mạng. Mở file `config.json` để cấu hình:
- `host`: Địa chỉ IP mạng (để `0.0.0.0` nếu muốn các máy khác trong mạng LAN truy cập được).
- `port`: Cổng chạy API (Mặc định `5000`).
- `threshold`: Ngưỡng quyết định (Mặc định `0.5`). Lớn hơn hoặc bằng mức này sẽ tính là Tích cực.

---

## 📡 3. Tài liệu API (API Documentation)

Bất kỳ hệ thống nào muốn sử dụng AI đều chỉ cần gọi HTTP POST vào endpoint này.

- **URL:** `http://localhost:5000/api/ai-chat`
- **Method:** `POST`
- **Content-Type:** `application/json`

### Dữ liệu gửi lên (Request Body)
```json
{
  "message": "Sản phẩm này thiết kế rất đẹp nhưng giá thì hơi chát và giao hàng chậm"
}
```

### Dữ liệu trả về (Response Body - Thành công 200 OK)
```json
{
  "status": "success",
  "reply": "🏷️ Phân loại: TIÊU CỰC (Tỉ lệ: 18.2%)\n💡 Giải thích: AI nhận diện được từ khen ('đẹp') và từ/cụm từ chê ('chậm')."
}
```

---

## 🔗 4. Hướng dẫn kết nối từ các ngôn ngữ Backend khác

Module AI này đóng vai trò như một máy chủ độc lập. Dưới đây là các ví dụ code copy-paste để Backend chính của dự án kết nối sang AI:

### ☕ Cấu hình cho Backend JAVA (Sử dụng `java.net.http.HttpClient` - Java 11+)
```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class AIChatClient {
    public static void main(String[] args) throws Exception {
        String jsonInput = "{\"message\": \"Sản phẩm này rất tuyệt vời\"}";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new URI("http://localhost:5000/api/ai-chat"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonInput))
                .build();

        HttpClient client = HttpClient.newHttpClient();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

        System.out.println("AI Phản hồi: " + response.body());
    }
}
```

### 🔷 Cấu hình cho Backend C# .NET (Sử dụng `HttpClient`)
```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program {
    static async Task Main() {
        using var client = new HttpClient();
        var json = "{\"message\": \"màn hình này dùng chán quá\"}";
        var content = new StringContent(json, Encoding.UTF8, "application/json");

        var response = await client.PostAsync("http://localhost:5000/api/ai-chat", content);
        var responseString = await response.Content.ReadAsStringAsync();

        Console.WriteLine("AI Phản hồi: " + responseString);
    }
}
```

### ⚙️ Cấu hình cho Backend C++ (Sử dụng thư viện `libcurl`)
```cpp
#include <iostream>
#include <curl/curl.h>

int main(void) {
  CURL *curl = curl_easy_init();
  if(curl) {
    // URL của module AI
    curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:5000/api/ai-chat");
    
    // Headers
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    
    // Body (JSON)
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "{\"message\": \"tốc độ xử lý rất nhanh và mượt\"}");

    // Gửi Request
    CURLcode res = curl_easy_perform(curl);
    
    // Dọn dẹp
    curl_easy_cleanup(curl);
  }
  return 0;
}
```

### 🌐 Kết nối trực tiếp từ Frontend (React / Vite / Vanilla JS)
*Lưu ý: API AI đã được bật sẵn thư viện CORS nên Frontend có thể gọi trực tiếp thông qua Fetch API.*
```javascript
fetch('http://localhost:5000/api/ai-chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: "dịch vụ ok, ngon lành" })
})
.then(res => res.json())
.then(data => console.log(data.reply))
.catch(err => console.error("Lỗi:", err));
```

### 💻 Test nhanh qua Terminal (Sử dụng cURL)
```bash
curl -X POST http://localhost:5000/api/ai-chat \
     -H "Content-Type: application/json" \
     -d "{\"message\": \"sản phẩm quá tệ\"}"
```
