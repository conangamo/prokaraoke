from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.song import Song
from app import db
from app.utils.decorators import login_required
from app.utils.helpers import save_image
from app.models.favorite import Favorite

song = Blueprint('song', __name__)

@song.route('/song/<int:song_id>')
def view_song(song_id):
    """Hiển thị chi tiết một bài hát"""
    song_item = Song.query.get_or_404(song_id)
    
    # Kiểm tra nếu bài hát đã bị xóa
    if song_item.is_deleted:
        flash('Bài hát này đã bị xóa!', 'warning')
        return redirect(url_for('main.home'))
    
    # Kiểm tra quyền truy cập nếu bài hát do admin đăng
    if song_item.is_admin_upload and not session.get('is_admin', False):
        flash('Bạn không phải admin, không thể xem chi tiết bài hát này!', 'danger')
        return redirect(url_for('main.home'))
    
    # Debug: Hiển thị đường dẫn ảnh
    print(f"DEBUG - Đường dẫn ảnh bài hát {song_id}: {song_item.image_path}")
        
    return render_template('song.html', song=song_item)

@song.route('/add', methods=['GET', 'POST'])
@login_required
def add_song():
    """Thêm bài hát mới"""
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist') or 'Unknown Artist'
        upload_type = request.form.get('upload_type', 'user')
        
        # Kiểm tra quyền nếu đăng bài dưới dạng admin
        if upload_type == 'admin' and not session.get('is_admin', False):
            flash('Bạn không có quyền đăng bài dưới dạng admin!', 'danger')
            return render_template('add.html')
        
        # Kiểm tra tên bài hát
        if not title:
            return render_template('add.html', error='Tên bài hát không được để trống!')
        
        # Xử lý file ảnh
        image_path = '/static/images/default_image.jpg'  # Đường dẫn mặc định
        
        if 'image' in request.files:
            file = request.files['image']
            saved_path = save_image(file)
            if saved_path:
                image_path = saved_path
        
        # Thêm bài hát vào cơ sở dữ liệu
        try:
            user_id = session.get('user_id')
            is_admin_upload = (upload_type == 'admin')
            
            new_song = Song(
                title=title, 
                artist=artist, 
                image_path=image_path,
                user_id=user_id,
                is_admin_upload=is_admin_upload
            )
            
            db.session.add(new_song)
            db.session.commit()
            flash(f'Đã thêm bài hát "{title}" thành công!', 'success')
            return redirect(url_for('song.view_song', song_id=new_song.id))
        except Exception as e:
            return render_template('add.html', error=f'Lỗi khi thêm bài hát: {str(e)}')
    
    return render_template('add.html')

@song.route('/edit/<int:song_id>', methods=['GET', 'POST'])
@login_required
def edit_song(song_id):
    """Chỉnh sửa thông tin bài hát"""
    song_item = Song.query.get_or_404(song_id)
    
    # Kiểm tra quyền chỉnh sửa (admin hoặc người tạo bài hát)
    if session.get('user_id') != song_item.user_id and not session.get('is_admin', False):
        flash('Bạn không có quyền chỉnh sửa bài hát này!', 'danger')
        return redirect(url_for('song.view_song', song_id=song_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        artist = request.form.get('artist') or 'Unknown Artist'
        
        # Kiểm tra tên bài hát
        if not title:
            flash('Tên bài hát không được để trống!', 'danger')
            return render_template('edit.html', song=song_item)
        
        # Xử lý file ảnh nếu có
        if 'image' in request.files:
            file = request.files['image']
            saved_path = save_image(file)
            if saved_path:
                song_item.image_path = saved_path
        
        # Cập nhật thông tin bài hát
        song_item.title = title
        song_item.artist = artist
        
        try:
            db.session.commit()
            flash(f'Đã cập nhật bài hát "{title}" thành công!', 'success')
            return redirect(url_for('song.view_song', song_id=song_id))
        except Exception as e:
            flash(f'Lỗi khi cập nhật bài hát: {str(e)}', 'danger')
            return render_template('edit.html', song=song_item)
    
    return render_template('edit.html', song=song_item)

@song.route('/delete/<int:song_id>')
@login_required
def delete_song(song_id):
    """Đưa bài hát vào thùng rác (soft delete)"""
    song_item = Song.query.get_or_404(song_id)
    
    # Kiểm tra quyền xóa (admin hoặc người tạo bài hát)
    if session.get('user_id') != song_item.user_id and not session.get('is_admin', False):
        flash('Bạn không có quyền xóa bài hát này!', 'danger')
        return redirect(url_for('song.view_song', song_id=song_id))
    
    # Đánh dấu xóa (đưa vào thùng rác)
    song_item.is_deleted = True
    
    try:
        db.session.commit()
        flash(f'Đã đưa bài hát "{song_item.title}" vào thùng rác!', 'success')
        return redirect(url_for('main.home'))
    except Exception as e:
        flash(f'Lỗi khi xóa bài hát: {str(e)}', 'danger')
        return redirect(url_for('song.view_song', song_id=song_id))

@song.route('/trash')
@login_required
def trash():
    """Hiển thị thùng rác"""
    # Admin xem tất cả bài hát trong thùng rác, user chỉ xem bài hát của mình
    if session.get('is_admin', False):
        songs = Song.query.filter_by(is_deleted=True).all()
    else:
        user_id = session.get('user_id')
        songs = Song.query.filter_by(is_deleted=True, user_id=user_id).all()
    
    return render_template('trash.html', songs=songs)

@song.route('/restore/<int:song_id>')
@login_required
def restore_song(song_id):
    """Khôi phục bài hát từ thùng rác"""
    song_item = Song.query.get_or_404(song_id)
    
    # Kiểm tra quyền khôi phục (admin hoặc người tạo bài hát)
    if session.get('user_id') != song_item.user_id and not session.get('is_admin', False):
        flash('Bạn không có quyền khôi phục bài hát này!', 'danger')
        return redirect(url_for('song.trash'))
    
    # Khôi phục bài hát
    song_item.is_deleted = False
    
    try:
        db.session.commit()
        flash(f'Đã khôi phục bài hát "{song_item.title}" thành công!', 'success')
        return redirect(url_for('song.trash'))
    except Exception as e:
        flash(f'Lỗi khi khôi phục bài hát: {str(e)}', 'danger')
        return redirect(url_for('song.trash'))

@song.route('/toggle_favorite/<int:song_id>')
@login_required
def toggle_favorite(song_id):
    """Thêm/bỏ bài hát vào/khỏi danh sách yêu thích"""
    song_item = Song.query.get_or_404(song_id)
    user_id = session.get('user_id')
    
    # Tìm kiếm bản ghi yêu thích
    favorite = Favorite.query.filter_by(user_id=user_id, song_id=song_id).first()
    
    try:
        if favorite:
            # Nếu đã yêu thích, xóa bỏ
            db.session.delete(favorite)
            message = f'Đã xóa bài hát "{song_item.title}" khỏi danh sách yêu thích!'
        else:
            # Nếu chưa yêu thích, thêm vào
            favorite = Favorite(user_id=user_id, song_id=song_id)
            db.session.add(favorite)
            message = f'Đã thêm bài hát "{song_item.title}" vào danh sách yêu thích!'
        
        db.session.commit()
        flash(message, 'success')
        
    except Exception as e:
        flash(f'Lỗi khi cập nhật trạng thái yêu thích: {str(e)}', 'danger')
    
    # Xác định trang trả về dựa trên HTTP_REFERER
    referer = request.headers.get('Referer')
    if referer:
        return redirect(referer)
    return redirect(url_for('song.view_song', song_id=song_id)) 