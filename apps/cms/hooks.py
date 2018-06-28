# -*- coding:utf-8 -*-
from .views import bp
from flask import session,g
from config import CMS_USER_ID
from .modles import CMSUser

@bp.before_request
def before_request():
    user_id = session.get(CMS_USER_ID)
    if user_id:
        user = CMSUser.query.get(user_id)
        if user:
            g.user = user
