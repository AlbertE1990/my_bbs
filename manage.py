# -*- coding:utf-8 -*-
from flask_migrate import Migrate,MigrateCommand
from exts import db
from my_bbs import app
from flask_script import Manager,Shell
from apps.cms.modles import CMSUser,CMSRole,CMSPermission,CmsRoleUser
from random import choice
import json


manager = Manager(app)
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option('-u','--user',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    return('CMS用户：%s,添加成功'%username)


@manager.command
def create_role():

    #1.访问者（修改个人信息）
    vistor = CMSRole(name='访问者',desc='只能访问相关数据')
    vistor.permissions = CMSPermission.VISTOR

    #2.运营员（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营员',desc='修改个人信息，管理帖子，管理评论，管理前台用户')
    operator.permissions = CMSPermission.VISTOR | CMSPermission.POSTER | \
                           CMSPermission.COMMENTER|CMSPermission.FRONTUSER


    #3.管理人员
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISTOR | CMSPermission.POSTER |\
                        CMSPermission.COMMENTER|CMSPermission.FRONTUSER |\
                        CMSPermission.BOARDER | CMSPermission.CMSUSER

    #4.开发者
    developer = CMSRole(name='开发者', desc='所有权限，开发者专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([vistor,operator,admin,developer])
    db.session.commit()
    return 'cms 角色创建成功！'


def make_shell_context():
    return dict(app=app, db=db, CMSUser=CMSUser, CMSRole=CMSRole,CmsRoleUser=CmsRoleUser,CMSPermission=CMSPermission)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def hello():
    return "hello world!"

#测试数据
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from faker import Faker
from apps.front.models import FrontUser
from apps.models import PostModel,CommentModel,BoardModel

fake = Faker(locale='zh_CN')

@manager.command
def front_users(count=30):
    i = 0
    while i < count:
        u = FrontUser(
            telephone = fake.phone_number(),
            email=fake.email(),
            username=fake.user_name(),
            password='password',
            realname=fake.name(),
            join_time=fake.past_datetime(),
            avatar=fake.image_url()
        )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
    return '前端用户数据生成成功！'

@manager.command
def posts(count=100):

    for i in range(count):
        author_id = FrontUser.query.order_by(func.rand()).limit(1).first().id
        board_id = BoardModel.query.order_by(func.rand()).limit(1).first().id
        p = PostModel(
            title = fake.paragraph(1),
            content=fake.text(),
            create_time=fake.past_datetime(),
            author_id=author_id,
            board_id=board_id
        )
        db.session.add(p)
    db.session.commit()
    return '帖子数据生成成功！'

@manager.command
def change_avatar():
    with open('avatar.json', 'r',encoding='utf-8') as f:
        imgs = json.load(f)

    front_users = FrontUser.query.all()
    for user in front_users:
        i = choice(imgs)
        try:
            user.avatar = i
            db.session.commit()
        except Exception as e:
            pass
    print('成功！')


if __name__ == '__main__':
    manager.run()