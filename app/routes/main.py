from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.song import Song
from app.models.favorite import Favorite
from app.utils.decorators import login_required
from sqlalchemy.sql import text
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Hiển thị trang chủ với phân trang"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 6  # Số bài hát trên mỗi trang
        songs = Song.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page)
        
        # Truyền thêm danh sách bài hát yêu thích của người dùng hiện tại
        favorite_songs = []
        if session.get('user_id'):
            # Lấy danh sách ID bài hát yêu thích của người dùng
            favorite_song_ids = db.session.query(Favorite.song_id)\
                .filter_by(user_id=session.get('user_id'))\
                .all()
            # Chuyển tuple thành list đơn giản
            favorite_songs = [item[0] for item in favorite_song_ids]
            
        return render_template('index.html', songs=songs, favorite_songs=favorite_songs)
    except Exception as e:
        return f'Kết nối cơ sở dữ liệu thất bại: {str(e)}'

@main.route('/search')
def search():
    """Tìm kiếm bài hát theo từ khóa"""
    query = request.args.get('query', '')
    search_type = request.args.get('search_type', 'title')  # Mặc định tìm theo tên bài hát
    
    if not query:
        return redirect(url_for('main.home'))
    
    try:
        # Tìm kiếm bài hát theo loại tìm kiếm (chỉ hiển thị bài hát chưa bị xóa)
        if search_type == 'artist':
            songs = Song.query.filter(Song.artist.ilike(f'%{query}%'), Song.is_deleted==False).all()
            search_type_text = "theo nghệ sĩ"
        else:  # search_type == 'title'
            songs = Song.query.filter(Song.title.ilike(f'%{query}%'), Song.is_deleted==False).all()
            search_type_text = "theo tên bài hát"
        
        # Truyền thêm danh sách bài hát yêu thích của người dùng hiện tại
        favorite_songs = []
        if session.get('user_id'):
            # Lấy danh sách ID bài hát yêu thích của người dùng
            favorite_song_ids = db.session.query(Favorite.song_id)\
                .filter_by(user_id=session.get('user_id'))\
                .all()
            # Chuyển tuple thành list đơn giản
            favorite_songs = [item[0] for item in favorite_song_ids]
            
        return render_template('search.html', songs=songs, query=query, 
                               search_type=search_type, search_type_text=search_type_text,
                               favorite_songs=favorite_songs)
    except Exception as e:
        return f'Lỗi khi tìm kiếm: {str(e)}' 

@main.route('/favorites')
@login_required
def favorites():
    """Hiển thị danh sách bài hát yêu thích"""
    # Lấy user_id hiện tại
    user_id = session.get('user_id')
    
    try:
        # Sử dụng join để lấy bài hát từ bảng Favorite
        songs = Song.query.join(Favorite, Song.id == Favorite.song_id)\
            .filter(Favorite.user_id == user_id, Song.is_deleted == False)\
            .all()
            
        return render_template('favorites.html', songs=songs)
    except Exception as e:
        return f'Lỗi khi lấy danh sách yêu thích: {str(e)}' 