# -*- coding:utf-8 -*-
from flask_migrate import Migrate,MigrateCommand
from exts import db
from my_bbs import app
from flask_script import Manager
from apps.cms.modles import CMSUser

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

if __name__ == '__main__':
    manager.run()