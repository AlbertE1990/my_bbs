from flask import  Blueprint,views,render_template,url_for,make_response,g,request,session,redirect,abort,flash
from utils.captcha import Captcha
from utils import my_redis,restful
from utils.my_redis import cache
from .forms import SignupForm,LoginForm,AddPostForm,AddCommentForm,PasswordResetRequestForm,PasswordResetForm
from .models import FrontUser
from exts import db,login_manager,mail
from flask_login import login_required,current_user
from config import FRONT_USER_ID,PER_PAGE
from ..models import BannerModel,BoardModel,PostModel,CommentModel,HighlightPostModel
from io import BytesIO
from flask_paginate import Pagination,get_page_parameter
from apps.email import send_email
from sqlalchemy import func

bp = Blueprint('front',__name__)
# bp = Blueprint('front',__name__)


@login_manager.user_loader
def load_user(user_id):
    return FrontUser.query.get(user_id)


@bp.app_template_filter('read_count')
def read_count(post):
    if cache.hget(post.id,'read_count'):
        return cache.hget(post.id,'read_count').decode('utf-8')
    return 0


#首页视图函数
@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=0)
    sort = request.args.get('sort',type=int,default=0)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start + PER_PAGE
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()

    if board_id:
        query_obj = PostModel.query.filter_by(board_id=board_id)
    else:
        query_obj = PostModel.query
        board_id = 0

    #按默认排序
    if sort == 0:
        pass
    #按帖子加精排序
    elif sort == 1:
        query_obj = query_obj.outerjoin(HighlightPostModel).order_by(
            HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    #按点赞最多排序
    elif sort ==2:
        pass
    # 按评论最多排序
    elif sort == 3:
        query_obj = query_obj.outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(),PostModel.create_time.desc())


    posts = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(page=page,total=total,bs_version=3)

    context = {
        'banners':banners,
        'boards':boards,
        'posts':posts,
        'pagination':pagination,
        'current_board':board_id,
        'current_sort':sort
    }
    return render_template('front/front_index.html',**context)


#确认邮箱邮件
def send_confirm(user,email):
    if user:
        token = user.generate_comfirmation_token()
        print(url_for('.confirm', token=token,_external=True))
        send_email(email, 'Mybbs账户确认邮箱',
                   'email/confirm',
                   user=user, token=token)
        return True
    return False


#注册视图函数
class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        return render_template('front/front_signup.html', return_to=return_to)
    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            email = form.email.data
            user = FrontUser(telephone=telephone, username=username, password=password, email=email)
            print(user)
            # db.session.add(user)
            # token = user.generate_comfirmation_token()
            # print(url_for('.confirm', token=token))
            # send_email(email, '确认邮箱',
            #            'email/confirm',
            #            user=user, token=token)
            # login_email = 'mail.'+email.split('@')[-1]
            # db.session.commit()
            return restful.success('ok')
        else:
            # message = form.get_error()
            # print('message:',message)
            print(form.errors)
            return restful.params_error('表单验证未通过')


@bp.route('/signup2/',methods=['post','get'])
def signup2():
    form = SignupForm()
    return_to = request.referrer
    if form.validate_on_submit():
        telephone = form.telephone.data
        username = form.username.data
        password = form.password1.data
        email = form.email.data
        user = FrontUser(telephone=telephone,username=username,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        session[FRONT_USER_ID] = user.id
        send_confirm(user,email)
        login_email = 'http://mail.'+email.split('@')[-1]
        return render_template('front/reigster_success.html', login_email=login_email)
    return render_template('front/front_signup2.html', return_to=return_to, signupform=form)


#登录视图函数
class LoginView(views.MethodView):

    def get(self):
        return_to = request.referrer
        current_url = request.url
        return render_template('front/front_login.html',return_to=return_to)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user:
                if user.check_password(password):
                    session[FRONT_USER_ID] = user.id
                    session.permanent = bool(remember)
                    return restful.success()
                else:
                    return restful.params_error('密码错误')
            else:
                return restful.params_error('此手机号码未注册！')

        else:
            print(form.errors)
            return restful.params_error()


#重置密码验证邮箱
class ResetPwdView(views.MethodView):

    def get(self):
        form = PasswordResetRequestForm()
        return render_template('front/front_resetpwd.html', form=form)

    def post(self):
        form = PasswordResetRequestForm(request.form)
        if form.validate:
            email = form.email.data
            user = FrontUser.query.filter_by(email=email).first()
            if user:
                token = user.generate_reset_token()
                my_redis.set(token,'Enable')
                send_email(user.email, '重置密码',
                           'email/reset_password',
                           user=user, token=token)
                flash('重置密码链接已发送到你邮箱，请注意查收')
            else:
                flash('该邮箱不存在')
        return redirect(url_for('.resetpwd'))


#未确认邮箱，拦截页面，等待从新发送确认邮件
@bp.route('/unconfirm/')
@login_required
def unconfirm():
    return render_template('front/unconfirm.html')


#重新发送确认邮件
@bp.route('/reconfirm/')
@login_required
def resend_confirmation():
    if send_confirm(current_user,current_user.email):
        flash('确认账户链接已发送到你邮箱，请注意查收')
    else:
        flash('邮件发送失败')
    return render_template('front/unconfirm.html')


#确认邮箱
@bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirm:
        flash('账户已经确认，无需重复确认，谢谢！')
    if current_user.confirm_token(token):
        flash('账户确认成功，谢谢！')
        db.session.commit()
    else:
        flash('账户确认链接失效，请从前发送链接')
    return redirect(url_for('.middle'))


#middle
@bp.route('/middle/')
def middle():
    return render_template('front/middle.html')


#重置密码
@bp.route('/resetpwd/<token>',methods=['GET', 'POST'])
def password_reset(token):
    if not my_redis.get(token):
        flash('该链接已经修改了密码，如需再次修改，请重新验证邮箱！')
        return redirect(url_for('.resetpwd'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        new_password = form.password.data
        if FrontUser.reset_password(token,new_password) and my_redis.get(token):
            db.session.commit()
            flash('密码重置成功')
            my_redis.delete(token)
            return redirect(url_for('.login'))
        else:
            flash('链接失效，请获取新链接')
    return render_template('front/front_resetpwd.html',form=form)


#注销视图函数
@bp.route('/logout/')
@login_required
def logout():
   session.clear()
   return redirect(url_for('front.index'))


#生成验证码
@bp.route('/captcha/')
def gene_captcha():
    text,image = Captcha.gene_graph_captcha()
    type = request.args.get('type')
    if type:
        session[type] = text
        print(type,text)
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


#检测验证码
@bp.route('/captcha/check/')
def check_captcha():       
    cap_type = request.args.get('type')
    cap_val = request.args.get('cap_val')
    if cap_val.lower() == session.get(cap_type).lower():
        return restful.success()
    else:
        return restful.params_error()


#添加帖子视图函数
class ApostView(views.MethodView):
    decorators = [login_required]
    def get(self):
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html',boards=boards)

    def post(self):
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title,content=content,board_id=board_id)
            post.author = current_user
            db.session.add(post)
            db.session.commit()
            return restful.success('帖子发布成功！')
        else:
            return restful.params_error(form.get_error())


#修改帖子
# class UpostView(views.MethodView):
#     decorators = [login_required]
#     def get(self,post_id):
#         post = PostModel.query.get_or_404(post_id)
#         boards = BoardModel.query.all()
#         return render_template('front/front_upost.html',boards=boards,post=post)
#
#     def post(self,post_id):
#         form = AddPostForm(request.form)
#         if form.validate():
#             post = PostModel.query.get_or_404(post_id)
#             title = form.title.data
#             content = form.content.data
#             board_id = form.board_id.data
#             post.title = title
#             post.board_id = board_id
#             post.content = content
#             db.session.add(post)
#             db.session.commit()
#             return restful.success('帖子修改成功！')
#         else:
#             return restful.params_error(form.get_error())

@bp.route('/upost/<post_id>',methods=['get','post'])
@login_required
def upost(post_id):
    post = PostModel.query.get_or_404(post_id)
    if not post.author == current_user:
        return render_template('front/front_error.html',error_msg='您无权修改此帖子'),403
    boards = BoardModel.query.all()
    form = AddPostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        board_id = form.board_id.data
        post.title = title
        post.board_id = board_id
        post.content = content
        db.session.add(post)
        db.session.commit()
        return restful.success('帖子修改成功！')
    return render_template('front/front_upost.html',boards=boards,post=post)


#帖子详情页面
@bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    if post:
        query_obj = CommentModel.query.filter(CommentModel.post_id == post_id).order_by(CommentModel.create_time.desc())
        comments = query_obj.slice(start, end)
        total = query_obj.count()
        pagination = Pagination(page=page, total=total, bs_version=3)
        context = {
            'post':post,
            'comments':comments,
            'pagination':pagination
        }

        cache.hincrby(post_id,'read_count')
        return render_template('front/front_post_detail.html',**context)
    else:
        abort(404)


#发表评论
@bp.route('/acomment/',methods=['Post'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        author_id = form.author_id.data
        comment = CommentModel(content=content,post_id=post_id,author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return restful.success('评论发表成功！')
    else:
        return restful.params_error(form.get_error())

#收藏帖子
@bp.route('/mark/')
@login_required
def mark():
    pid = request.args.get('post_id')
    book_status = request.args.get('book_status')
    user = g.get('front_user')
    if not user:
        return restful.params_error('请先登陆！')
    post = PostModel.query.get(pid)
    if post:
        if book_status == 'book':
            user.bookmark.append(post)
            db.session.add(user)
            db.session.commit()
            return restful.success('收藏成功')
        else:
            print(user.bookmark)
            user.bookmark.remove(post)
            db.session.add(user)
            db.session.commit()
            return restful.success('取消收藏成功')
    else:
        return restful.params_error('未找到该帖子！')

#个人信息
@bp.route('/profile/<uid>/')
def profile(uid):
    user = FrontUser.query.get(uid)
    if not uid:
        abort(404)
    return render_template('front/profile.html',cuser=user)

#显示书签收藏信息
@bp.route('/bookmark/<uid>/')
def bookmark(uid):
    user = FrontUser.query.get(uid)
    if not user:
        abort(404)
    posts = user.bookmark
    return render_template('front/bookmark.html', cuser=user,posts=posts)

#我的帖子
@bp.route('/myposts/<uid>/')
def myposts(uid):
    user = FrontUser.query.get(uid)
    if not user:
        abort(404)
    posts = user.posts
    return render_template('front/myposts.html', cuser=user,posts=posts)

#关注用户
@bp.route('/follow/<uid>')
def follow(uid):
    current_user = g.get('front_user')
    if not current_user:
        return restful.unauth_error('请先登录')
    user = FrontUser.query.get(uid)
    if not user:
        return restful.params_error('当前用户不存在')
    if current_user.is_following(user):
        return restful.params_error('已经关注该用户')
    current_user.follow(user)
    db.session.commit()
    return restful.success('关注成功')

#取消关注
@bp.route('/unfollow/<uid>')
@login_required
def unfollow(uid):
    user = FrontUser.query.get(uid)
    if not user:
        return restful.params_error('当前用户不存在')
    if not current_user.is_following(user):
        return restful.params_error('您还没有关注该用户')
    current_user .unfollow(user)
    db.session.commit()
    return restful.success('取消关注成功')

#显示关注着
@bp.route('/followers/<uid>')
def followers(uid):
    user = FrontUser.query.get_or_404(uid)
    user_followers = user.followers
    pass


bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/apost/',view_func=ApostView.as_view('apost'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
# bp.add_url_rule('/upost/<post_id>',view_func=UpostView.as_view('upost'))


