# -*- coding:utf-8 -*-
from flask import Blueprint

bp = Blueprint('front',__name__,url_prefix='/')

@bp.route('/')
def indext():
    return 'Hello word!front_index'