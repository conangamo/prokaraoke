from flask import Blueprint, render_template, redirect, url_for, flash
from app.models.song import Song
from app import db
from app.utils.decorators import admin_required

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@admin_required
def admin_panel():
    """Hiển thị trang quản trị admin"""
    # Hiển thị bài hát được đăng bởi admin
    songs = Song.query.filter_by(is_admin_upload=True, is_deleted=False).all()
    return render_template('admin.html', songs=songs)

@admin.route('/permanent_delete/<int:song_id>')
@admin_required
def permanent_delete(song_id):
    """Xóa vĩnh viễn bài hát (chỉ admin)"""
    song_item = Song.query.get_or_404(song_id)
    
    try:
        db.session.delete(song_item)
        db.session.commit()
        flash(f'Đã xóa vĩnh viễn bài hát "{song_item.title}" thành công!', 'success')
        return redirect(url_for('song.trash'))
    except Exception as e:
        flash(f'Lỗi khi xóa vĩnh viễn bài hát: {str(e)}', 'danger')
        return redirect(url_for('song.trash'))

@admin.route('/users')
@admin_required
def manage_users():
    """Quản lý người dùng (dành cho tương lai mở rộng)"""
    flash('Chức năng này sẽ được phát triển trong tương lai!', 'info')
    return redirect(url_for('admin.admin_panel')) 