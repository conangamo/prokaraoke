from app import db
from datetime import datetime

class Favorite(db.Model):
    """Model Favorite đại diện cho mối quan hệ yêu thích giữa người dùng và bài hát"""
    __tablename__ = 'Favorites'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('Songs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Định nghĩa ràng buộc duy nhất cho cặp user_id và song_id
    __table_args__ = (db.UniqueConstraint('user_id', 'song_id', name='unique_user_song'),)
    
    def __init__(self, user_id, song_id):
        self.user_id = user_id
        self.song_id = song_id
    
    def __repr__(self):
        return f"<Favorite: User {self.user_id} - Song {self.song_id}>" 