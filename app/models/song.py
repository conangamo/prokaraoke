from app import db

class Song(db.Model):
    """Model Song đại diện cho bài hát trong hệ thống"""
    __tablename__ = 'Songs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), default='Unknown Artist')
    image_path = db.Column(db.String(255), default='/static/images/default_image.jpg')
    
    # Foreign key và các cờ kiểm soát
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    is_admin_upload = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, artist, user_id=None, image_path='/static/images/default_image.jpg', 
                is_admin_upload=False, is_deleted=False, is_favorite=False):
        self.title = title
        self.artist = artist
        self.image_path = image_path
        self.user_id = user_id
        self.is_admin_upload = is_admin_upload
        self.is_deleted = is_deleted
        self.is_favorite = is_favorite
    
    def serialize(self):
        """Chuyển đổi đối tượng thành từ điển để trả về API"""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'image_path': self.image_path,
            'user_id': self.user_id,
            'is_admin_upload': self.is_admin_upload,
            'is_deleted': self.is_deleted,
            'is_favorite': self.is_favorite
        }
    
    def __repr__(self):
        return f"<Song {self.title} by {self.artist}>" 