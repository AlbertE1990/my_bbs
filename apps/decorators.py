from functools import wraps
from flask import session,redirect,url_for,request,render_template,abort
from flask_login import current_user,login_required
from flask_login.utils import login_url
from utils import restful

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated:
            return func(*args,**kwargs)
        else:
            if request.is_xhr:
                return restful.unauth_error('请先进行登陆')
            current_bp = request.blueprint
            login_view = current_bp+'.login'
            redirect_url = login_url(url_for(login_view),next_url=request.url)
            return redirect(redirect_url)
    return wrapper

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                if request.is_xhr:
                    return restful.permission_error('无此权限')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

