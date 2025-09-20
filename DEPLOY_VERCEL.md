# Hướng dẫn Deploy dự án lên Vercel

## Bước 1: Chuẩn bị dự án

Dự án đã được chuẩn bị sẵn với các file cần thiết:
- ✅ `vercel.json` - Cấu hình Vercel
- ✅ `wsgi.py` - WSGI entry point
- ✅ `requirements.txt` - Dependencies đã được tối ưu
- ✅ `.vercelignore` - Loại bỏ file không cần thiết
- ✅ `app.py` - Ứng dụng Flask chính

## Bước 2: Tạo tài khoản Vercel

1. Truy cập [vercel.com](https://vercel.com)
2. Đăng ký/Đăng nhập bằng GitHub, GitLab hoặc Bitbucket
3. Kết nối với tài khoản Git của bạn

## Bước 3: Deploy từ GitHub (Khuyến nghị)

### 3.1. Tạo repository GitHub
```bash
# Khởi tạo git repository
git init

# Thêm tất cả file
git add .

# Commit lần đầu
git commit -m "Initial commit: PDF Randomizer app"

# Tạo repository trên GitHub và push
git remote add origin https://github.com/username/pdf-randomizer.git
git branch -M main
git push -u origin main
```

### 3.2. Deploy trên Vercel
1. Đăng nhập vào [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import repository từ GitHub
4. Vercel sẽ tự động detect Flask app
5. Click **"Deploy"**

## Bước 4: Deploy từ máy local (Alternative)

### 4.1. Cài đặt Vercel CLI
```bash
# Cài đặt Vercel CLI
npm install -g vercel

# Hoặc sử dụng npx
npx vercel
```

### 4.2. Deploy
```bash
# Đăng nhập Vercel
vercel login

# Deploy dự án
vercel

# Deploy production
vercel --prod
```

## Bước 5: Cấu hình Environment Variables

Trong Vercel Dashboard, thêm environment variables:

1. Vào **Project Settings** → **Environment Variables**
2. Thêm biến:
   - `GEMINI_API_KEY`: API key của Google Gemini
   - `FLASK_ENV`: `production`

## Bước 6: Kiểm tra deployment

1. Sau khi deploy thành công, bạn sẽ nhận được URL
2. Truy cập URL để test ứng dụng
3. Kiểm tra các tính năng:
   - ✅ Trang chủ hiển thị
   - ✅ Random dữ liệu
   - ✅ Tải PDF

## Cấu trúc file sau khi chuẩn bị

```
tool veo3/
├── app.py                 # Ứng dụng Flask chính
├── wsgi.py               # WSGI entry point cho Vercel
├── vercel.json           # Cấu hình Vercel
├── requirements.txt      # Dependencies
├── .vercelignore         # File bỏ qua khi deploy
├── templates/
│   └── index.html        # Giao diện web
├── tool.pdf              # File PDF gốc
└── DEPLOY_VERCEL.md      # Hướng dẫn này
```

## Lưu ý quan trọng

### 1. API Key Gemini
- **KHÔNG** commit API key vào Git
- Sử dụng Environment Variables trong Vercel
- Thay đổi API key trong code thành:
```python
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-default-key'))
```

### 2. File PDF
- File `tool.pdf` sẽ được upload cùng với code
- Đảm bảo file có kích thước hợp lý (< 50MB)

### 3. Performance
- Vercel có giới hạn execution time (10s cho Hobby plan)
- Nếu xử lý PDF mất thời gian, có thể cần upgrade plan

## Troubleshooting

### Lỗi "Module not found"
- Kiểm tra `requirements.txt` có đầy đủ dependencies
- Đảm bảo không có conflicts trong versions

### Lỗi "File not found"
- Kiểm tra đường dẫn file PDF trong code
- Đảm bảo file `tool.pdf` được upload

### Lỗi "API key not found"
- Kiểm tra Environment Variables trong Vercel
- Đảm bảo tên biến chính xác

### Timeout errors
- Optimize code xử lý PDF
- Consider upgrade Vercel plan
- Cache kết quả nếu có thể

## URL sau khi deploy

Sau khi deploy thành công, bạn sẽ có URL dạng:
```
https://pdf-randomizer-xxx.vercel.app
```

## Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Vercel Dashboard → Functions → Logs
2. GitHub Actions (nếu sử dụng)
3. Environment Variables
4. File structure

---

**Chúc bạn deploy thành công! 🚀**
