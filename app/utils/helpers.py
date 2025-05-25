import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Kiểm tra tệp có phải là loại được cho phép không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    """Lưu tệp hình ảnh và trả về đường dẫn"""
    if file and file.filename != '' and allowed_file(file.filename):
        try:
            # Kiểm tra nếu file rỗng
            file.seek(0, os.SEEK_END)
            size = file.tell()
            if size == 0:
                print(f"WARNING: File {file.filename} rỗng")
                return None
            file.seek(0)  # Reset con trỏ file về đầu
            
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)
            
            # Kiểm tra lại file sau khi lưu
            if os.path.getsize(file_path) == 0:
                print(f"WARNING: File đã lưu {file_path} rỗng, xóa file")
                os.remove(file_path)
                return None
                
            # Trả về đường dẫn tương đối để lưu trong cơ sở dữ liệu
            return '/static/images/' + unique_filename
        except Exception as e:
            print(f"ERROR: Lỗi khi lưu file: {str(e)}")
            return None
    
    return None 