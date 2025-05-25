from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from config import config
import os

# Cấu hình để sử dụng pymysql với SQLAlchemy
pymysql.install_as_MySQLdb()

# Khởi tạo các extension
db = SQLAlchemy()

def create_app(config_name='default'):
    """Tạo và cấu hình ứng dụng Flask"""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config[config_name])
    
    # Khởi tạo các extension với app
    db.init_app(app)
    
    # Đảm bảo thư mục upload tồn tại
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Đăng ký các blueprint
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.song import song
    from app.routes.admin import admin
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(song)
    app.register_blueprint(admin)
    
    return app 