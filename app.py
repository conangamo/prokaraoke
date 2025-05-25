import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.utils import secure_filename

# Cấu hình để sử dụng pymysql với SQLAlchemy
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'karaoke_secret_key'  # Cần thiết cho flash messages

# Cấu hình upload file
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Cấu hình kết nối cơ sở dữ liệu
mysql_user = os.environ.get('MYSQL_USER', 'user')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'password')
mysql_host = os.environ.get('MYSQL_HOST', 'db')
mysql_db = os.environ.get('MYSQL_DB', 'karaoke_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Định nghĩa model Song
class Song(db.Model):
    __tablename__ = 'Songs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), default='Unknown Artist')
    image_path = db.Column(db.String(255), default='static/images/default_image.jpg')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    try:
        # Thử kết nối đến cơ sở dữ liệu và truy vấn dữ liệu
        songs = Song.query.all()
        return render_template('index.html', songs=songs)
    except Exception as e:
        return f'Kết nối cơ sở dữ liệu thất bại: {str(e)}'

@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist') or 'Unknown Artist'
        
        # Kiểm tra tên bài hát
        if not title:
            return render_template('add.html', error='Tên bài hát không được để trống!')
        
        # Xử lý file ảnh
        image_path = 'static/images/default_image.jpg'  # Đường dẫn mặc định
        
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '' and file:
                if allowed_file(file.filename):
                    # Tạo tên file an toàn với uuid để tránh trùng lặp
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                    
                    try:
                        file.save(file_path)
                        image_path = f'static/images/{unique_filename}'
                    except Exception as e:
                        return render_template('add.html', error=f'Lỗi khi lưu file: {str(e)}')
                else:
                    return render_template('add.html', error='Chỉ chấp nhận file PNG, JPG hoặc JPEG!')
        
        # Thêm bài hát vào cơ sở dữ liệu
        try:
            new_song = Song(title=title, artist=artist, image_path=image_path)
            db.session.add(new_song)
            db.session.commit()
            return render_template('add.html', success=f'Đã thêm bài hát "{title}" thành công!')
        except Exception as e:
            return render_template('add.html', error=f'Lỗi khi thêm bài hát: {str(e)}')
    
    return render_template('add.html')

@app.route('/search')
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'title')  # Mặc định tìm theo tên bài hát
    
    if not query:
        return redirect(url_for('home'))
    
    try:
        # Tìm kiếm bài hát theo loại tìm kiếm
        if search_type == 'artist':
            songs = Song.query.filter(Song.artist.ilike(f'%{query}%')).all()
            search_type_text = "theo nghệ sĩ"
        else:  # search_type == 'title'
            songs = Song.query.filter(Song.title.ilike(f'%{query}%')).all()
            search_type_text = "theo tên bài hát"
            
        return render_template('search.html', songs=songs, query=query, search_type=search_type, search_type_text=search_type_text)
    except Exception as e:
        return f'Lỗi khi tìm kiếm: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)