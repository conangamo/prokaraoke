from flask import Blueprint, render_template, request, redirect, url_for
from app.models.song import Song
from app.utils.decorators import login_required

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Hiển thị trang chủ với phân trang"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 6  # Số bài hát trên mỗi trang
        songs = Song.query.filter_by(is_deleted=False).paginate(page=page, per_page=per_page)
        return render_template('index.html', songs=songs)
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
            
        return render_template('search.html', songs=songs, query=query, 
                               search_type=search_type, search_type_text=search_type_text)
    except Exception as e:
        return f'Lỗi khi tìm kiếm: {str(e)}' 

@main.route('/favorites')
@login_required
def favorites():
    """Hiển thị danh sách bài hát yêu thích"""
    # Hiển thị bài hát yêu thích và không bị xóa
    songs = Song.query.filter_by(is_favorite=True, is_deleted=False).all()
    return render_template('favorites.html', songs=songs) 