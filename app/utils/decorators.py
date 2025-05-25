from functools import wraps
from flask import redirect, url_for, flash, session

def login_required(f):
    """Decorator để kiểm tra người dùng đã đăng nhập hay chưa"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục!', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator để kiểm tra người dùng có quyền admin hay không"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục!', 'warning')
            return redirect(url_for('auth.login'))
        if not session.get('is_admin', False):
            flash('Bạn không có quyền truy cập trang này!', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function 