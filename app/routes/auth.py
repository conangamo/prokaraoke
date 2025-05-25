from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app.models.user import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Xử lý đăng nhập người dùng"""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Chào mừng {user.username}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'danger')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Xử lý đăng ký người dùng mới"""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        secret_key = request.form.get('secret_key', '')
        
        # Kiểm tra mật khẩu xác nhận
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp!', 'danger')
            return render_template('register.html')
        
        # Kiểm tra username đã tồn tại chưa
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Tên đăng nhập đã tồn tại!', 'danger')
            return render_template('register.html')
        
        # Xác định quyền admin
        is_admin = False
        if secret_key == '123':
            is_admin = True
        
        # Tạo user mới
        try:
            new_user = User(username=username, password=password, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Đăng ký thất bại: {str(e)}', 'danger')
    
    return render_template('register.html')

@auth.route('/logout')
def logout():
    """Đăng xuất người dùng"""
    session.clear()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('main.home'))

@auth.route('/profile')
def profile():
    """Hiển thị thông tin người dùng"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        session.clear()
        flash('Tài khoản không tồn tại!', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user) 