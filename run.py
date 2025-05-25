import os
from app import create_app, db
import time
import platform
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# Tạo ứng dụng với cấu hình mặc định hoặc từ biến môi trường
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Tạo context ứng dụng để chạy flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

def wait_for_db(max_retries=5, retry_interval=3):
    """
    Thử kết nối đến database và chờ đến khi thành công hoặc đạt giới hạn thử lại.
    """
    retries = 0
    while retries < max_retries:
        try:
            print(f"Thử kết nối đến database (lần {retries + 1})...")
            # Thử truy xuất database với cú pháp text() của SQLAlchemy
            with app.app_context():
                with db.engine.connect() as connection:
                    result = connection.execute(text("SELECT 1"))
                    print(f"Kết quả truy vấn: {result.fetchone()}")
            print("Kết nối thành công đến database!")
            return True
        except OperationalError as e:
            retries += 1
            print(f"Lỗi kết nối OperationalError: {str(e)}")
            if retries >= max_retries:
                print(f"Không thể kết nối đến database sau {max_retries} lần thử")
                return False
            print(f"Thử lại sau {retry_interval} giây...")
            time.sleep(retry_interval)
        except SQLAlchemyError as e:
            retries += 1
            print(f"Lỗi SQLAlchemy: {str(e)}")
            if retries >= max_retries:
                print(f"Không thể kết nối đến database sau {max_retries} lần thử")
                return False
            print(f"Thử lại sau {retry_interval} giây...")
            time.sleep(retry_interval)
        except Exception as e:
            retries += 1
            print(f"Lỗi không xác định: {str(e)}")
            if retries >= max_retries:
                print(f"Không thể kết nối đến database sau {max_retries} lần thử")
                return False
            print(f"Thử lại sau {retry_interval} giây...")
            time.sleep(retry_interval)

# Chỉ chạy ứng dụng khi gọi trực tiếp file này
if __name__ == '__main__':
    # Hiển thị thông tin môi trường
    is_docker = os.environ.get('DOCKER_ENV') == 'true'
    env_type = "Docker container" if is_docker else f"Local ({platform.system()})"
    db_host = app.config.get('SQLALCHEMY_DATABASE_URI').split('@')[1].split('/')[0]
    
    print(f"======================================================")
    print(f"Khởi động ứng dụng karaoke trong môi trường: {env_type}")
    print(f"Sử dụng cơ sở dữ liệu: {db_host}")
    if is_docker:
        print(f"Truy cập ứng dụng tại: http://localhost:5001")
    else:
        print(f"Truy cập ứng dụng tại: http://localhost:5000")
    print(f"======================================================")
    
    # Thử kết nối database
    wait_for_db(max_retries=10, retry_interval=5)
    
    try:
        # Tạo tất cả bảng nếu chưa tồn tại
        print("Tạo bảng database nếu chưa tồn tại...")
        with app.app_context():
            db.create_all()
        print("Tạo bảng database hoàn tất!")
    except Exception as e:
        print(f"Lỗi khi tạo bảng: {str(e)}")
        
    print("Khởi động ứng dụng web...")
    app.run(host='0.0.0.0', port=5000, debug=True) 