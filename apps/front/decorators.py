from functools import wraps
from flask import session,redirect,url_for,request,render_template
from  config import FRONT_USER_ID
from flask_login import current_user

# def login_required(func):
#     @wraps(func)
#     def wrapper(*args,**kwargs):
#         if session.get(FRONT_USER_ID):
#             return func(*args,**kwargs)
#         else:
#             return redirect(url_for('front.login'))
#     return wrapper

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator