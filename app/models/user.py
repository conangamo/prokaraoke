from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# Bảng quan hệ nhiều-nhiều giữa User và Song cho tính năng yêu thích
favorites = db.Table('Favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('Songs.id'), primary_key=True),
    db.Column('created_at', db.DateTime, server_default=db.func.now())
)

class User(db.Model):
    """Model User đại diện cho người dùng trong hệ thống"""
    __tablename__ = 'Users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Thiết lập relationship one-to-many với Song
    songs = db.relationship('Song', backref='user', lazy=True)
    
    # Thiết lập relationship many-to-many với Song cho tính năng yêu thích
    favorite_songs = db.relationship('Song', 
                                     secondary=favorites, 
                                     lazy='subquery',
                                     backref=db.backref('favorited_by', lazy=True))
    
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    
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