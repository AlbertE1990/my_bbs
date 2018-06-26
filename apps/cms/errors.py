# -*- coding:utf-8 -*-
# from .views import bp
#
# @bp.app_errorhandler(404)
# def page_not_fount(e):
#     return 'page not found haha!',404
import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
x = os.path.join(base_path,'templates/cms/cms_profile_ajax.html')
print(os.path.isfile(x))
