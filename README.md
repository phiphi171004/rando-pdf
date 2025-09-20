# PDF Randomizer Web App

Web app tự động random thông tin trong PDF và tải về file mới với giao diện đẹp.

## Tính năng

- ✅ **Web app đơn giản** - Chỉ cần mở trình duyệt
- ✅ **Tự động random** tất cả thông tin cần thiết
- ✅ **Preview trước khi tải** - Xem dữ liệu sẽ được random
- ✅ **Tải PDF ngay lập tức** - Không cần import file
- ✅ **Giao diện đẹp** - Responsive, modern UI
- ✅ **Sử dụng file tool.pdf** - Tự động lấy file gốc

## Cài đặt

### Yêu cầu hệ thống
- Python 3.7 trở lên
- Windows/Linux/macOS

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Chạy ứng dụng

```bash
# Cách 1: Chạy script tự động
run_web.bat

# Cách 2: Chạy thủ công
python app.py
```

Sau đó mở trình duyệt và truy cập: **http://localhost:5000**

## Hướng dẫn sử dụng

### 1. Khởi động Web App
- Chạy `run_web.bat` hoặc `python app.py`
- Mở trình duyệt và truy cập `http://localhost:5000`

### 2. Sử dụng Web App
- **Xem trước dữ liệu**: Click "👁️ Xem trước dữ liệu" để xem dữ liệu sẽ được random
- **Random & Tải PDF**: Click "🎲 Random & Tải PDF" để tạo PDF mới và tải về

### 3. Các trường được random tự động:
- **Barcode No**: Random 6 số (ví dụ: 937675)
- **Name**: Random tên đầy đủ
- **Father's Name**: Random tên bố
- **Mother's Name**: Random tên mẹ
- **Mailing Address**: Random địa chỉ Delhi
- **User**: Random 6 số
- **Receipt No**: Giữ "25-6-", random 6 số cuối
- **SOL Roll No**: Giữ "25-6-02-", random 6 số cuối
- **Date of Birth**: Giữ năm, random ngày tháng
- **Phone No**: Random 10 số
- **Refe.No**: Random 9 số
- **Email ID**: Tự động tạo từ tên + SOL Roll No

### 4. Tải PDF
- Sau khi random, click "📥 Tải PDF về máy"
- File sẽ được tải về với tên "randomized_document.pdf"

## Ví dụ dữ liệu được random

```
Barcode No: 937675
Name: John Smith
Father's Name: David Johnson
Mother's Name: Sarah Williams
Mailing Address: Connaught Place, New Delhi
User: 123456
Receipt No: 25-6-789012
SOL Roll No: 25-6-02-345678
Date of Birth: 15-08-2000
Phone No: 9876543210
Refe.No: 123456789
Email ID: john25-6-02-345678@sol.du.ac.in
```

## Cấu trúc dự án

```
tool veo3/
├── app.py                  # Web app Flask chính
├── templates/
│   └── index.html         # Giao diện web
├── requirements.txt        # Danh sách thư viện cần thiết
├── run_web.bat            # Script chạy web app
├── tool.pdf               # File PDF gốc để random
└── README.md              # Hướng dẫn sử dụng
```

## Thư viện sử dụng

- **Flask**: Web framework
- **PyMuPDF (fitz)**: Xử lý PDF, đọc/ghi file PDF
- **PIL (Pillow)**: Xử lý hình ảnh

## Lưu ý

- Web app tự động sử dụng file `tool.pdf` có sẵn
- Không cần import file, chỉ cần click random
- Dữ liệu được random theo logic cụ thể
- File PDF mới được tạo tự động và tải về

## Xử lý lỗi thường gặp

### Lỗi "File PDF gốc không tồn tại"
- Đảm bảo file `tool.pdf` có trong thư mục
- Kiểm tra tên file chính xác

### Lỗi "Lỗi kết nối"
- Kiểm tra web app đã chạy chưa
- Truy cập đúng địa chỉ `http://localhost:5000`
- Kiểm tra firewall/antivirus

### Lỗi "Không thể tải file"
- Kiểm tra quyền ghi file
- Thử tải lại trang web
- Kiểm tra dung lượng ổ đĩa

---

**Chúc bạn sử dụng tool hiệu quả! 🎉**
