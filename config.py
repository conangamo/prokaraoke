import os
import platform
import socket

class Config:
    """Cấu hình cơ bản của ứng dụng"""
    SECRET_KEY = 'karaoke_secret_key'
    
    # Cấu hình upload file
    UPLOAD_FOLDER = 'app/static/images'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Kiểm tra xem đang chạy trong Docker hay không
    IS_DOCKER = os.environ.get('DOCKER_ENV') == 'true'
    
    # Cấu hình cơ sở dữ liệu
    MYSQL_USER = os.environ.get('MYSQL_USER', 'user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'karaoke_db')
    
    # Xác định host dựa trên môi trường
    if IS_DOCKER:
        # Trong Docker sử dụng tên service
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')
        MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    else:
        # Môi trường phát triển local, sử dụng port mapping
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_PORT = os.environ.get('MYSQL_PORT', '3308')
    
    # Cấu hình kết nối SQLAlchemy
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Cấu hình cho môi trường phát triển"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Cấu hình cho môi trường sản xuất"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-key'

# Cấu hình mặc định
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 