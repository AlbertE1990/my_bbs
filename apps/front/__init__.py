from flask import Blueprint


bp = Blueprint('front',__name__,subdomain='front')
# bp = Blueprint('front',__name__,url_prefix='/front')


from . import hooks,views,errors
