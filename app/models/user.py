from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """Model User đại diện cho người dùng trong hệ thống"""
    __tablename__ = 'Users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Thiết lập relationship one-to-many với Song
    songs = db.relationship('Song', backref='user', lazy=True)
    
    # Thiết lập relationship one-to-many với Favorite
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    
    # Kiểm tra xem người dùng đã yêu thích bài hát nào chưa
    def has_favorited(self, song_id):
        from app.models.favorite import Favorite
        return Favorite.query.filter_by(user_id=self.id, song_id=song_id).first() is not None
    
    # Lấy tất cả bài hát yêu thích của người dùng
    def get_favorite_songs(self):
        from app.models.song import Song
        from app.models.favorite import Favorite
        favorites = Favorite.query.filter_by(user_id=self.id).all()
        return [Song.query.get(fav.song_id) for fav in favorites]
    
    def check_password(self, password):
        """Kiểm tra mật khẩu"""
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        """Kiểm tra người dùng đã xác thực chưa"""
        return True
    
    def is_active(self):
        """Kiểm tra người dùng có hoạt động không"""
        return True
    
    def is_anonymous(self):
        """Kiểm tra người dùng có ẩn danh không"""
        return False
    
    def get_id(self):
        """Trả về id của người dùng"""
        return str(self.id)
    
    def __repr__(self):
        return f"<User {self.username}>" 