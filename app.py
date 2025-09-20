#!/usr/bin/env python3
"""
PDF Randomizer Web App
Tự động random các thông tin trong PDF và tải về
"""

from flask import Flask, render_template, send_file, request, jsonify
import fitz  # PyMuPDF
import random
import string
import os
import tempfile
import io
from datetime import datetime, timedelta
import re
import google.generativeai as genai
import json

app = Flask(__name__)

# Cấu hình Gemini API
genai.configure(api_key="AIzaSyDlAcOmSNTycoGqgCw2pCz79onaY_LMadg")
model = genai.GenerativeModel('gemini-1.5-flash')

# Danh sách địa chỉ Delhi để random
DELHI_ADDRESSES = [
    "Connaught Place, New Delhi",
    "Karol Bagh, New Delhi", 
    "Lajpat Nagar, New Delhi",
    "Rajouri Garden, New Delhi",
    "Pitampura, New Delhi",
    "Dwarka, New Delhi",
    "Rohini, New Delhi",
    "Janakpuri, New Delhi",
    "Vasant Kunj, New Delhi",
    "Saket, New Delhi",
    "Greater Kailash, New Delhi",
    "Hauz Khas, New Delhi",
    "Malviya Nagar, New Delhi",
    "Defence Colony, New Delhi",
    "South Extension, New Delhi"
]

# Danh sách tên để random
FIRST_NAMES = [
    "Aarav", "Arjun", "Vikram", "Rahul", "Suresh", "Rajesh", "Amit", "Vikash",
    "Priya", "Anita", "Sunita", "Kavita", "Rekha", "Meera", "Sita", "Gita",
    "John", "Mike", "David", "Chris", "Alex", "Sam", "Tom", "Ben",
    "Sarah", "Emma", "Lisa", "Anna", "Kate", "Jane", "Mary", "Lucy"
]

LAST_NAMES = [
    "Sharma", "Singh", "Kumar", "Gupta", "Verma", "Yadav", "Patel", "Jain",
    "Agarwal", "Malhotra", "Chopra", "Bansal", "Goyal", "Khanna", "Saxena", "Tiwari",
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Taylor"
]

def generate_names_with_gemini():
    """Generate tên khác nhau bằng Gemini API"""
    try:
        prompt = """
        Generate 3 different Indian names (student, father, mother) in JSON format:
        {
            "student": "First Last",
            "father": "First Last", 
            "mother": "First Last"
        }
        Make sure all 3 names are completely different. Use common Indian names.
        Return only the JSON, no other text.
        """
        
        response = model.generate_content(prompt)
        print(f"Gemini response: {response.text}")  # Debug
        
        # Tìm JSON trong response
        text = response.text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        
        result = json.loads(text.strip())
        
        return {
            'student': result.get('student', 'John Smith'),
            'father': result.get('father', 'Mike Johnson'),
            'mother': result.get('mother', 'Sarah Davis')
        }
    except Exception as e:
        print(f"Lỗi Gemini API: {e}")
        # Fallback to random names với logic đảm bảo khác nhau
        student_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        
        father_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        while father_name == student_name:
            father_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        
        mother_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        while mother_name == student_name or mother_name == father_name:
            mother_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        
        return {
            'student': student_name,
            'father': father_name,
            'mother': mother_name
        }

def generate_random_data():
    """Tạo dữ liệu random cho tất cả các trường"""
    # Random barcode (6 số)
    barcode = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Generate tên bằng Gemini API
    names = generate_names_with_gemini()
    full_name = names['student']
    father_name = names['father']
    mother_name = names['mother']
    
    # Lấy first name cho email
    first_name = full_name.split()[0]
    
    # Random Mailing Address
    mailing_address = random.choice(DELHI_ADDRESSES)
    
    # Random User (6 số)
    user_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Random Receipt No (giữ 25-6, random 6 số cuối)
    receipt_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    receipt_no = f"25-6-{receipt_suffix}"
    
    # Tạo SOL Roll No trước (giữ 25-6-02-04, random 4 số cuối)
    roll_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    sol_roll_no = f"25-6-02-04{roll_suffix}"
    
    # Random Date of Birth (giữ năm, random ngày tháng)
    year = 2000  # Giữ nguyên năm
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Đảm bảo ngày hợp lệ
    
    # Chuyển tháng thành tên
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }
    month_name = month_names[month]
    date_of_birth = f"{day:02d}-{month_name}-{year}"
    
    # Random Phone No (10 số)
    phone_no = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    # Random Refe.No (9 số)
    refe_no = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Tạo Email ID từ first name + SOL Roll No (giữ dấu -)
    # Đảm bảo dãy số trong email giống hệt SOL Roll No
    email_id = f"{first_name.lower()}{sol_roll_no}@sol.du.ac.in"
    
    # Debug: In ra để kiểm tra
    print(f"SOL Roll No: {sol_roll_no}")
    print(f"Email ID: {email_id}")
    print(f"First name: {first_name}")
    print(f"Roll suffix (4 số): {roll_suffix}")
    print(f"Email ID chỉ có dãy số: {first_name.lower()}{sol_roll_no}")
    
    return {
        'barcode': barcode,
        'name': full_name,
        'father_name': father_name,
        'mother_name': mother_name,
        'mailing_address': mailing_address,
        'user_number': user_number,
        'receipt_no': receipt_no,
        'sol_roll_no': sol_roll_no,
        'roll_suffix': roll_suffix,  # Thêm roll_suffix để sử dụng trong replacements
        'date_of_birth': date_of_birth,
        'phone_no': phone_no,
        'refe_no': refe_no,
        'email_id': email_id
    }

def replace_text_in_pdf(pdf_path, replacements, random_data):
    """Thay thế text trong PDF"""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Lấy tất cả text để debug
        all_text = page.get_text()
        print(f"Page {page_num + 1} text: {all_text[:200]}...")  # Debug
        
        # Xử lý riêng cho Barcode và User (cả 2 đều dùng 'RANDOM 6 SỐ')
        barcode_user_instances = page.search_for('RANDOM 6 SỐ')
        print(f"Tìm thấy {len(barcode_user_instances)} instances của 'RANDOM 6 SỐ'")  # Debug
        
        for i, rect in enumerate(barcode_user_instances):
            if i == 0:
                # Instance đầu tiên là Barcode
                new_text = random_data['barcode']
                print(f"Thay thế Barcode (instance {i+1}): '{new_text}' tại vị trí: {rect}")  # Debug
            elif i == 1:
                # Instance thứ 2 là User
                new_text = random_data['user_number']
                print(f"Thay thế User (instance {i+1}): '{new_text}' tại vị trí: {rect}")  # Debug
            
            try:
                # Xóa text cũ
                expanded_rect = fitz.Rect(rect.x0 - 2, rect.y0 - 2, rect.x1 + 2, rect.y1 + 2)
                page.add_redact_annot(expanded_rect, fill=(1, 1, 1))
                page.apply_redactions()
                
                # Thêm text mới
                x = rect.x0
                y = rect.y1 - 2
                page.insert_text((x, y), new_text, fontsize=7.5)
                print(f"Đã thêm text mới: '{new_text}'")  # Debug
                
            except Exception as e:
                print(f"Lỗi thay thế text: {e}")

        # Xử lý riêng cho tên (Name, Father's Name, Mother's Name)
        if 'RANDOM TÊN TÂY' in replacements:
            # Tìm tất cả instances của 'RANDOM TÊN TÂY'
            text_instances = page.search_for('RANDOM TÊN TÂY')
            print(f"Tìm thấy {len(text_instances)} instances của 'RANDOM TÊN TÂY'")  # Debug
            
            # Thay thế từng instance với tên khác nhau
            # Lấy tên từ random_data
            names = [replacements['RANDOM TÊN TÂY'], random_data['father_name'], random_data['mother_name']]
            
            for i, rect in enumerate(text_instances):
                if i < len(names):
                    new_text = names[i]
                    print(f"Thay thế instance {i+1}: '{new_text}' tại vị trí: {rect}")  # Debug
                    
                    try:
                        # Xóa text cũ
                        expanded_rect = fitz.Rect(rect.x0 - 2, rect.y0 - 2, rect.x1 + 2, rect.y1 + 2)
                        page.add_redact_annot(expanded_rect, fill=(1, 1, 1))
                        page.apply_redactions()
                        
                        # Thêm text mới
                        x = rect.x0
                        y = rect.y1 - 2
                        page.insert_text((x, y), new_text, fontsize=7.5)
                        print(f"Đã thêm text mới: '{new_text}'")  # Debug
                        
                    except Exception as e:
                        print(f"Lỗi thay thế text: {e}")
        
        # Xử lý riêng cho SOL Roll No trước (chỉ thay thế field SOL Roll No, không phải trong email)
        # Tìm chính xác text "25-6-02-048878" không có ký tự khác
        sol_roll_instances = page.search_for('25-6-02-048878')
        print(f"Tìm thấy {len(sol_roll_instances)} instances của SOL Roll No")  # Debug
        
        for rect in sol_roll_instances:
            # Lấy text hiện tại để kiểm tra
            current_text = page.get_textbox(rect)
            print(f"SOL Roll No hiện tại: '{current_text}'")  # Debug
            
            # Chỉ thay thế nếu đây là SOL Roll No field chính xác (không có ký tự khác)
            if current_text.strip() == '25-6-02-048878':
                new_sol_roll = random_data['sol_roll_no']
                print(f"Thay thế SOL Roll No: '{current_text}' -> '{new_sol_roll}'")  # Debug
                
                try:
                    # Xóa text cũ
                    expanded_rect = fitz.Rect(rect.x0 - 2, rect.y0 - 2, rect.x1 + 2, rect.y1 + 2)
                    page.add_redact_annot(expanded_rect, fill=(1, 1, 1))
                    page.apply_redactions()
                    
                    # Thêm text mới
                    x = rect.x0
                    y = rect.y1 - 2
                    page.insert_text((x, y), new_sol_roll, fontsize=7.5)
                    print(f"Đã thêm SOL Roll No mới: '{new_sol_roll}'")  # Debug
                    
                except Exception as e:
                    print(f"Lỗi thay thế SOL Roll No: {e}")
            else:
                print(f"Bỏ qua SOL Roll No: '{current_text}' (không phải field chính)")

        # Xử lý các replacements khác
        for old_text, new_text in replacements.items():
            if old_text == 'RANDOM TÊN TÂY':
                continue  # Đã xử lý ở trên
            if old_text == 'RANDOM 6 SỐ':
                continue  # Đã xử lý Barcode và User ở trên
            if old_text == '25-6-02-048878':
                continue  # Đã xử lý SOL Roll No ở trên
                
            print(f"Tìm kiếm: '{old_text}' -> '{new_text}'")  # Debug
            
            # Tìm tất cả instances của text cũ
            text_instances = page.search_for(old_text)
            print(f"Tìm thấy {len(text_instances)} instances")  # Debug
            
            if len(text_instances) == 0:
                # Thử tìm kiếm không phân biệt hoa thường
                text_instances = page.search_for(old_text, flags=fitz.TEXT_DEHYPHENATE)
                print(f"Tìm kiếm không phân biệt hoa thường: {len(text_instances)} instances")
            
            # Nếu vẫn không tìm thấy và text có chứa "firstname", thử tìm text có chứa "firstname"
            if len(text_instances) == 0 and 'firstname' in old_text:
                print(f"Thử tìm text có chứa 'firstname'...")  # Debug
                # Tìm tất cả text có chứa "firstname"
                all_text = page.get_text()
                lines = all_text.split('\n')
                for line in lines:
                    if 'firstname' in line and '@sol.du.ac.in' in line:
                        print(f"Tìm thấy dòng có firstname và @sol.du.ac.in: {line}")  # Debug
                        # Tìm text trong dòng này
                        text_instances = page.search_for(line.strip())
                        if len(text_instances) > 0:
                            print(f"Tìm thấy {len(text_instances)} instances của dòng")  # Debug
                            break
            
            # Nếu vẫn không tìm thấy và text có pattern 25-6-02-, thử tìm text có pattern này
            if len(text_instances) == 0 and '25-6-02-' in old_text:
                print(f"Thử tìm text có pattern 25-6-02-...")  # Debug
                # Tìm tất cả text có pattern 25-6-02-
                all_text = page.get_text()
                lines = all_text.split('\n')
                for line in lines:
                    if '25-6-02-' in line:
                        print(f"Tìm thấy dòng có 25-6-02-: {line}")  # Debug
                        # Tìm text trong dòng này
                        text_instances = page.search_for(line.strip())
                        if len(text_instances) > 0:
                            print(f"Tìm thấy {len(text_instances)} instances của dòng")  # Debug
                            break
            
            # Nếu vẫn không tìm thấy và text có đuôi @sol.du.ac.in, thử tìm text có đuôi này
            if len(text_instances) == 0 and '@sol.du.ac.in' in old_text:
                print(f"Thử tìm text có đuôi @sol.du.ac.in...")  # Debug
                # Tìm tất cả text có đuôi @sol.du.ac.in
                all_text = page.get_text()
                lines = all_text.split('\n')
                for line in lines:
                    if '@sol.du.ac.in' in line:
                        print(f"Tìm thấy dòng có @sol.du.ac.in: {line}")  # Debug
                        # Tìm text trong dòng này
                        text_instances = page.search_for(line.strip())
                        if len(text_instances) > 0:
                            print(f"Tìm thấy {len(text_instances)} instances của dòng")  # Debug
                            break
            
            for rect in text_instances:
                print(f"Thay thế tại vị trí: {rect}")  # Debug
                
                # Lấy font size và style từ text gốc trước khi xóa
                font_size = 7.5  # Font size cố định như yêu cầu
                font_name = "helv"
                try:
                    text_dict = page.get_text("dict")
                    for block in text_dict["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    if old_text.lower() in span["text"].lower():
                                        font_size = span.get("size", 12)
                                        font_name = span.get("font", "helv")
                                        print(f"Font: {font_name}, Size: {font_size}")  # Debug
                                        break
                except Exception as e:
                    print(f"Lỗi lấy font: {e}")
                    pass
                
                try:
                    # Xóa text cũ bằng cách vẽ hình chữ nhật trắng rộng hơn
                    expanded_rect = fitz.Rect(rect.x0 - 2, rect.y0 - 2, rect.x1 + 2, rect.y1 + 2)
                    page.add_redact_annot(expanded_rect, fill=(1, 1, 1))
                    page.apply_redactions()
                    
                    # Thêm text mới với font size và style giống text gốc
                    x = rect.x0
                    y = rect.y1 - 2
                    
                    # Thêm text mới với font size chính xác
                    page.insert_text((x, y), new_text, fontsize=font_size, fontname=font_name)
                    print(f"Đã thêm text mới: '{new_text}' với font {font_name} size {font_size}")  # Debug
                    
                except Exception as e:
                    print(f"Lỗi thay thế text: {e}")
                    # Fallback: thử với font mặc định
                    try:
                        page.insert_text((rect.x0, rect.y1 - 2), new_text, fontsize=7.5)
                        print(f"Đã thêm text mới (fallback): '{new_text}'")
                    except Exception as e2:
                        print(f"Lỗi fallback: {e2}")
    
    return doc

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/randomize', methods=['POST'])
def randomize_pdf():
    """Random PDF và trả về file mới"""
    try:
        # Xóa file cũ trước khi tạo file mới
        cleanup_temp_files()
        
        # Tạo dữ liệu random
        random_data = generate_random_data()
        
        # Debug: In ra quy trình tạo SOL Roll No và Email ID
        print(f"=== QUY TRÌNH TẠO DỮ LIỆU ===")
        print(f"1. SOL Roll No được tạo: {random_data['sol_roll_no']}")
        print(f"2. First name: {random_data['name'].split()[0]}")
        print(f"3. Email ID được tạo: {random_data['email_id']}")
        print(f"4. Roll suffix: {random_data['roll_suffix']}")
        print(f"5. Email ID cho replacement: {random_data['name'].split()[0].lower()}{random_data['sol_roll_no']}@sol.du.ac.in")
        print(f"================================")
        
        # Đường dẫn file PDF gốc
        original_pdf = 'tool.pdf'
        
        if not os.path.exists(original_pdf):
            return jsonify({'error': 'File PDF gốc không tồn tại!'}), 400
        
        # Tạo replacements dictionary với text chính xác từ PDF
        replacements = {
            # Name - chỉ thay thế 1 lần đầu tiên
            'RANDOM TÊN TÂY': random_data['name'],
            
            # Mailing Address - thay thế toàn bộ dòng
            'A 25, RANDOM DELHI ADDRESS, DELHI - 110027': random_data['mailing_address'],
            
            # Receipt No
            '25-06-876823': random_data['receipt_no'],
            
            # SOL Roll No - sẽ được xử lý riêng trong replace_text_in_pdf
            
            # Date of Birth - tìm text chính xác từ PDF
            '01-Jan-2004': random_data['date_of_birth'],
            
            # Phone No - tìm text chính xác từ PDF
            '9878287675': random_data['phone_no'],
            
            # Refe.No
            'RANDOM 9 SỐ': random_data['refe_no'],
            
            # Email ID - tìm text chính xác từ PDF
            'firstname25-6-02-048878@sol.du.ac.in': random_data['email_id'],
            
            # Dòng cuối - thay thế email và phone trong dòng cuối
            'Liam25-6-02-048878@sol.du.ac.in': random_data['email_id'],
            'sam25602221042@sol.du.ac.in': random_data['email_id'],  # Thêm biến thể khác
            '9878287675': random_data['phone_no']
        }
        
        # Debug: In ra replacements dictionary
        print(f"=== REPLACEMENTS DICTIONARY ===")
        for key, value in replacements.items():
            print(f"'{key}' -> '{value}'")
        print(f"================================")
        
        # Tạo PDF mới
        doc = replace_text_in_pdf(original_pdf, replacements, random_data)
        
        # Tạo tên file unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"randomized_{timestamp}.pdf"
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        # Lưu file
        doc.save(temp_path)
        doc.close()
        
        return jsonify({
            'success': True,
            'data': random_data,
            'download_url': f'/download/{filename}',
            'preview_url': f'/preview_pdf/{filename}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Tải file PDF đã random"""
    try:
        # Tìm file trong thư mục temp
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        if os.path.exists(temp_path):
            # Đọc file và gửi về
            with open(temp_path, 'rb') as f:
                file_data = f.read()
            
            # KHÔNG xóa file ngay lập tức - để user có thể tải lại
            # File sẽ được xóa bởi cleanup_temp_files() sau 1 giờ
            
            return send_file(
                io.BytesIO(file_data),
                as_attachment=True,
                download_name='randomized_document.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({'error': 'File không tồn tại!'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Lỗi tải file: {str(e)}'}), 500

@app.route('/preview', methods=['POST'])
def preview_data():
    """Preview dữ liệu random trước khi tải"""
    try:
        random_data = generate_random_data()
        return jsonify({'success': True, 'data': random_data})
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/preview_pdf/<filename>')
def preview_pdf(filename):
    """Preview PDF file"""
    try:
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        if os.path.exists(temp_path):
            return send_file(temp_path, mimetype='application/pdf')
        else:
            return jsonify({'error': 'File không tồn tại! File có thể đã bị xóa sau 1 giờ.'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Lỗi preview: {str(e)}'}), 500

@app.route('/check_file/<filename>')
def check_file(filename):
    """Kiểm tra file có tồn tại không"""
    try:
        temp_path = os.path.join(tempfile.gettempdir(), filename)
        
        if os.path.exists(temp_path):
            # Lấy thông tin file
            file_size = os.path.getsize(temp_path)
            file_time = datetime.fromtimestamp(os.path.getmtime(temp_path))
            
            return jsonify({
                'exists': True,
                'size': file_size,
                'created': file_time.strftime('%Y-%m-%d %H:%M:%S'),
                'message': 'File sẵn sàng tải! File sẽ được giữ lại cho đến khi bạn random kết quả mới.'
            })
        else:
            return jsonify({
                'exists': False,
                'message': 'File không tồn tại! File đã bị xóa khi bạn random kết quả mới.'
            })
            
    except Exception as e:
        return jsonify({'error': f'Lỗi kiểm tra file: {str(e)}'}), 500

@app.route('/debug')
def debug_pdf():
    """Debug: Xem tất cả text trong PDF gốc"""
    try:
        doc = fitz.open('tool.pdf')
        all_text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            all_text += f"=== PAGE {page_num + 1} ===\n{text}\n\n"
        
        doc.close()
        return f"<pre>{all_text}</pre>"
        
    except Exception as e:
        return f"Lỗi debug: {str(e)}"

def cleanup_temp_files():
    """Dọn dẹp file tạm cũ - xóa tất cả file randomized cũ"""
    try:
        temp_dir = tempfile.gettempdir()
        for filename in os.listdir(temp_dir):
            if filename.startswith('randomized_') and filename.endswith('.pdf'):
                file_path = os.path.join(temp_dir, filename)
                try:
                    # Xóa tất cả file randomized cũ
                    os.remove(file_path)
                    print(f"Đã xóa file cũ: {filename}")
                except:
                    pass
    except:
        pass

if __name__ == '__main__':
    # Dọn dẹp file tạm khi khởi động
    cleanup_temp_files()
    app.run(debug=True, host='0.0.0.0', port=5000)
