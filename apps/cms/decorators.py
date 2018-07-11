from functools import wraps
from flask import session,redirect,url_for,g,render_template
from flask_login import current_user


# def login_required(func):
#     @wraps(func)
#     def wrapper(*args,**kwargs):
#         if session.get(CMS_USER_ID):
#             return func(*args,**kwargs)
#         else:
#             return redirect(url_for('cms.login'))
#     return wrapper


def permission(p):
    def dec(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('permission decorate print')
            print(current_user.role.permissions )
            print(p)
            if current_user.role.permissions & p == p:
                return func(*args, **kwargs)
            else:
                return render_template('cms/forbidden.html'),403
        return  wrapper
    return dec





