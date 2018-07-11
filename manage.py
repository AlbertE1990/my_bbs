# -*- coding:utf-8 -*-
from flask_migrate import Migrate,MigrateCommand
from exts import db
from my_bbs import app
from flask_script import Manager,Shell
from apps.cms.modles import CMSUser,CMSRole,CMSPermission,CmsRoleUser

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


if __name__ == '__main__':
    manager.run()