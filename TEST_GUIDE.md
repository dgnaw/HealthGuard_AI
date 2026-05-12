
## 🧪 Hướng dẫn Kiểm tra Mô hình AI (Testing Guide)


Tài liệu này hướng dẫn các kịch bản nhập liệu để kiểm tra khả năng phân tích cảm xúc của mô hình **Logistic Regression**.

## 🎯 1. Các nhóm từ khóa mà AI nhận diện
Mô hình được huấn luyện dựa trên bộ từ điển (Lexicon) sau:
- **Tích cực (Positive):** `tốt`, `hay`, `tuyệt`, `đẹp`, `ok`, `thích`, `ngon`.
- **Tiêu cực (Negative):** `tệ`, `chán`, `xấu`, `lỗi`, `hỏng`, `dở`, `chậm`, `kém`.
- **Cụm từ phủ định (Negation):** `không tốt`, `chưa hay`, `không đẹp`, `không thích`,...

---

## 📝 2. Các kịch bản thử nghiệm (Test Cases)

Hãy nhập các câu sau vào giao diện Chat để kiểm tra phản hồi của AI:

### Kịch bản 1: Khen ngợi đơn giản
- **Câu nhập:** "Sản phẩm này dùng rất tốt và tuyệt vời"
- **Kỳ vọng:** Label TÍCH CỰC. Giải thích sẽ chỉ ra từ 'tốt' và 'tuyệt'.

### Kịch bản 2: Chê bai (Tiêu cực)
- **Câu nhập:** "Máy chạy rất chậm, hay bị lỗi và chán"
- **Kỳ vọng:** Label TIÊU CỰC. Giải thích sẽ chỉ ra từ 'chậm', 'lỗi', 'chán'.

### Kịch bản 3: Xử lý phủ định (Nâng cao)
- **Câu nhập:** "Dịch vụ khách hàng không tốt lắm"
- **Kỳ vọng:** AI phải nhận diện được cụm `không tốt` là Tiêu cực thay vì chỉ nhìn thấy chữ `tốt`.

### Kịch bản 4: Câu hỗn hợp (Phức tạp)
- **Câu nhập:** "Thiết kế rất đẹp nhưng pin dùng hơi tệ và chậm"
- **Kỳ vọng:** AI sẽ liệt kê cả từ khen ('đẹp') và từ chê ('tệ', 'chậm') sau đó đưa ra kết quả dựa trên tổng điểm trọng số.

---

## 💡 3. Cách đọc kết quả AI
Mỗi phản hồi của AI sẽ bao gồm:
1. **🏷️ Phân loại:** Kết quả cuối cùng (Tích cực/Tiêu cực) kèm xác suất % (tính từ hàm Sigmoid).
2. **💡 Giải thích:** Minh bạch hóa các từ khóa mà AI đã "nhìn thấy" trong câu để đưa ra quyết định. Điều này giúp kiểm chứng thuật toán chạy đúng logic đếm từ và nhân trọng số.


