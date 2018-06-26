from functools import wraps
from flask import session,redirect,url_for
from config import CMS_USER_ID

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get(CMS_USER_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return wrapper