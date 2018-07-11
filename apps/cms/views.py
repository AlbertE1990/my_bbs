# -*- coding:utf-8 -*-
from flask import Blueprint,render_template,request,session,redirect,url_for,g
from flask.views import MethodView
from .forms import LoginForm,ResetPasswordForm,ProfileForm,ResetEmailForm,validate_email,RegisterForm
from .modles import CMSUser,CMSUserDetail,CMSPermission
from utils import restful,my_redis
from config import CMS_USER_ID
from .decorators import permission
from exts import db,mail
import string
import random
from flask_mail import Message
from flask_login import login_required,login_user,logout_user

bp = Blueprint('cms',__name__,url_prefix='/cms')


import os
base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))




@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


#登陆
class LoginView(MethodView):

    def get(self):
        return render_template('cms/cms_login.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # session[CMS_USER_ID] = user.id
                # session.permanent = remember
                login_user(user)
                return restful.success(message='登录成功!')
            else:
                return restful.params_error(message='邮箱或者密码错误！')

        else:
            print(form.errors)
            return restful.params_error(message= '邮箱或者密码格式错误！')


#注销
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.login'))


#个人信息
class ProfileView(MethodView):
    decorators = [login_required]


    def get(self):
        return render_template('cms/cms_profile.html')

    def post(self):
        #有待优化
        detail = g.user.detail
        form = ProfileForm(request.form)
        if form.validate():
            data = {}
            data['uid'] = g.user.id
            data['name'] = form.name.data
            data['phone'] = form.phone.data
            data['birthday'] = form.birthday.data
            data['gender'] = form.gender.data
            data['intro'] = form.intro.data
            data['avatar'] = form.avatar.data
            d = {}
            for k, v in data.items():
                if v != '':
                    d[k] = v
            if detail:
                detail.name = d.get('name')
                detail.phone = d.get('phone')
                detail.birthday = d.get('birthday')
                detail.gender = d.get('gender')
                detail.intro = d.get('intro')
                detail.avatar = d.get('avatar')
            else:
                detail = CMSUserDetail(**d)
            db.session.add(detail)
            db.session.commit()
            return restful.success('信息保存成功！')
        else:
            print(form.errors)
            return restful.params_error('信息保存失败！')

bp.add_url_rule('/profile', view_func=ProfileView.as_view('profile'))


#修改密码
class ResetPasswordView(MethodView):

    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPasswordForm(request.form)
        if form.validate():
            raw_pwd = form.raw_pwd.data
            new_pwd = form.new_pwd1.data
            if g.user.check_password(raw_pwd):
                g.user.password = new_pwd
                return restful.success('密码修改成功！')
            else:
                return restful.params_error('原始密码错误！')
        else:
            return restful.params_error('原始密码错误!')



#修改邮箱
class ResetEmailView(MethodView):
    decorators = [login_required,]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            g.user.email = form.email.data
            db.session.commit()
            return restful.success(message='邮箱修改成功！')
        else:
            print(form.errors)
            return restful.params_error(message='数据错误！')


#邮箱验证码
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    email = request.args.get('email')
    validate_res = validate_email(email)
    if not validate_res['flag']:
        return restful.params_error(message=validate_res['message'])

    source = list(string.ascii_lowercase) + list(string.digits)
    captcha = "".join(random.sample(source, 6))
    body = '您的验证码是：%s,验证码有效期为5分钟' % captcha
    message = Message('CMS管理后台邮件发送', recipients=[email], body=body)
    my_redis.set(email,captcha,ex=300)
    print('生成的验证码',captcha)

    try:
        mail.send(message=message)
    except:
        return restful.server_error()
    return restful.success(message="邮件发送成功请注意查收！")


#cms用户管理
@bp.route('/cms_users/')
@login_required
@permission(CMSPermission.CMSUSER)
def cms_users():
    users = CMSUser.query.all()
    return render_template('cms/cms_user_manage.html',users=users)


#注册cms用户

def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()


@bp.route('/cms_register/',methods=['post'])
@login_required
@permission(CMSPermission.CMSUSER)
def cms_register():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.new_pwd1.data
        create_cms_user(username=username, password=password, email=email)
        return restful.success(message='添加新用户成功！')
    else:
        print(form.errors)
        return restful.params_error(message='注册数据有问题')


#帖子管理
@bp.route('/posts/')
@login_required
@permission(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

# #帖子管理
# @bp.route('/posts/')
# @login_required
# def posts():
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     PER_PAGE  = config.CMS_PER_PAGE
#     start = (page-1)*PER_PAGE
#     end = start+PER_PAGE
#     query_obj = PostModel.query.order_by(PostModel.create_time.desc())
#     posts = query_obj.slice(start,end)
#     total = query_obj.count()
#     pagination = Pagination(page=page,total=total,bs_version=3)
#     context = {
#         'posts': posts,
#         'pagination': pagination
#     }
#     return render_template('cms/cms_posts.html',**context)

# #删帖
# @bp.route('/dpost/',methods=['post'])
# @login_required
# def dposts():
#     post_id = request.form.get('post_id')
#     if not post_id:
#         return restful.params_error('此帖子ID不存在')
#     post = PostModel.query.get(post_id)
#     if not post:
#         return restful.params_error('未找到此帖子')
#     db.session.delete(post)
#     db.session.commit()
#     return restful.success('删帖成功！')
#
# #帖子加精
# @bp.route('/hpost/',methods=['POST'])
# @login_required
# def hpost():
#     post_id = request.form.get('post_id')
#     if not post_id:
#         return restful.params_error('此帖子ID不存在')
#     post = PostModel.query.get(post_id)
#     if not post:
#         return restful.params_error('未找到此帖子')
#     highlight = HighlightPostModel(post_id=post_id)
#     db.session.add(highlight)
#     db.session.commit()
#     return restful.success('加精成功！')
#
# #帖子取消加精
# @bp.route('/uhpost/',methods=['post'])
# @login_required
# def uhpost():
#     post_id = request.form.get('post_id')
#     print('post_id:',post_id)
#     if not post_id:
#         return restful.params_error('此帖子ID不存在')
#     post = PostModel.query.get(post_id)
#     if not post:
#         return restful.params_error('未找到此帖子')
#     highlight = post.highlight[0]
#     print('delete highlight:',highlight)
#     db.session.delete(highlight)
#     db.session.commit()
#     print('取消加精成功！')
#     return restful.success('取消加精成功！')

#评论管理
@bp.route('/comments/')
@login_required
@permission(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

#板块管理
@bp.route('/boards/')
@login_required
@permission(CMSPermission.BOARDER)
def boards():
    # boards = BoardModel.query.all()
    return render_template('cms/cms_boards.html')

# #添加板块
# @bp.route('/aboard/',methods=['POST'])
# @login_required
# def aboard():
#     form = AddBoardForm(request.form)
#     if form.validate():
#         name = form.name.data
#         board = BoardModel(name=name)
#         db.session.add(board)
#         db.session.commit()
#         return restful.success('板块添加成功！')
#
# #修改板块
# @bp.route('/uboard/',methods=['POST'])
# @login_required
# def uboard():
#     form = AddBoardForm(request.form)
#     if form.validate():
#         name = form.name.data
#         id = form.id.data
#         board = BoardModel.query.get(id)
#         if board:
#             board.name = name
#             db.session.commit()
#             return restful.success('板块修改成功！')
#         else:
#             return restful.params_error('此板块ID未查询到！')
#
# #删除板块
# @bp.route('/dboard/',methods=['POST'])
# @login_required
# def dboard():
#     form = request.form
#     id = form.get('id')
#     board = BoardModel.query.get(id)
#     if board:
#         db.session.delete(board)
#         db.session.commit()
#         return restful.success('板块删除成功！')
#     else:
#         return restful.params_error('删除失败，此板块ID未查询到！')


#轮播图管理
@bp.route('/banners/')
@login_required
@permission(CMSPermission.BOARDER)
def banners():
    # banners = BannerModel.query.order_by(BannerModel.priority.desc())
    return render_template('cms/cms_banners.html')


# #轮播图添加
# @bp.route('/abanners/',methods=['POST'])
# @login_required
# def abanners():
#     form = AddBannerForm(request.form)
#     if form.validate():
#         name = form.name.data
#         image_url = form.image_url.data
#         link_url = form.link_url.data
#         priority = form.priority.data
#         banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
#         db.session.add(banner)
#         db.session.commit()
#         return restful.success('轮播图信息添加成功！')
#     else:
#         return restful.params_error(form.get_error())
#
#
# #轮播图修改
# @bp.route('/ubanners/',methods=['POST'])
# @login_required
# def ubanners():
#     form = AddBannerForm(request.form)
#     if form.validate():
#         name = form.name.data
#         image_url = form.image_url.data
#         link_url = form.link_url.data
#         priority = form.priority.data
#         id = form.id.data
#         banner = BannerModel.query.get(id)
#
#         if banner:
#             banner.name = name
#             banner.image_url = image_url
#             banner.link_url = link_url
#             banner.priority = priority
#             db.session.commit()
#             return restful.success('轮播图信息修改成功！')
#         else:
#             return restful.server_error('没有这个轮播图')
#     else:
#         return restful.params_error(form.get_error())
#
#
# #轮播图删除
# @bp.route('/dbanners/',methods=['GET'])
# @login_required
# def dbanners():
#     id = request.args.get('id')
#     banner = BannerModel.query.get(id)
#     if banner:
#         db.session.delete(banner)
#         db.session.commit()
#         return restful.success('轮播图删除成功！')
#     else:
#         return restful.params_error('未查询到此轮播图ID！')





bp.add_url_rule('/resetpwd',view_func=ResetPasswordView.as_view('resetpwd'))
bp.add_url_rule('/resetemail',view_func=ResetEmailView.as_view('resetemail'))
bp.add_url_rule('/login/',endpoint='login',view_func=LoginView.as_view('login'))

@bp.context_processor
def cms_context_processor():
    return{'CMSPermission':CMSPermission}