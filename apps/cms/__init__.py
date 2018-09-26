# -*- coding:utf-8 -*-
from flask import Blueprint


bp = Blueprint('cms',__name__,subdomain='cms')

# bp = Blueprint('cms',__name__,url_prefix='/cms')

from . import views