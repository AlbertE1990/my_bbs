from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from faker import Faker
from apps.models import Apply,PostModel,CommentModel,BoardModel,User,GenderEnum,Role,Permission
from random import choice,randint
import json
from exts import db


fake = Faker(locale='zh_CN')


def front_user(count=10):
    fake = Faker(locale='zh_CN')
    n=0
    for i in range(count):
        u = User()
        u.telephone = fake.phone_number()
        u.username = fake.user_name()
        u.email = fake.ascii_free_email()
        u.password = 'password'
        u.confirm = choice([True,False])
        u.realname = fake.name()
        with open('mxavatar.json','r') as f:
            avatar_list = json.load(f)
        u.avatar = choice(avatar_list)
        u.signature = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        u.gender = GenderEnum(randint(1,4))
        u.join_time = fake.date_this_year(before_today=True, after_today=False)
        role = Role()
        u.role = role
        db.session.add(u)
        try:
            db.session.commit()
            n += 1
        except Exception:
            db.session.rollback()
    print('Front用户添加成功，共同添加%d个用户' % n)


def posts(count=50):
    count = int(count)
    for i in range(count):
        author_id = User.query.order_by(func.rand()).limit(1).first().id
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


def change_avatar():
    with open('avatar.json', 'r',encoding='utf-8') as f:
        imgs = json.load(f)

    front_users = User.query.all()
    for user in front_users:
        i = choice(imgs)
        try:
            user.avatar = i
            db.session.commit()
        except Exception as e:
            pass
    print('成功！')


def comments():
    posts = PostModel.query.all()
    authors = User.query.all()
    for post in posts:
        count = randint(1,200)
        for i in range(count-1):
            comment = CommentModel(
                content = fake.text(),
                create_time = fake.past_datetime(),
                post_id = post.id,
                author_id= choice(authors).id
            )
            db.session.add(comment)
        db.session.commit()
    print('评论生成成功！')


def boards(count):
    for _ in range(count):
        board = BoardModel()
        board.name = fake.word()
        board.create_time = fake.past_datetime()
        db.session.add(board)
    db.session.commit()
    print('版块生成成功！')


def test_group_user():
    roles = ['FrontUser','Operator','Administrator','Super']
    msg={}
    for r in roles:
        role = Role(group=r)
        u = User()
        u.telephone = fake.phone_number()
        u.username = r+'-test'
        u.email = fake.ascii_free_email()
        u.password = 'password'
        u.confirm = True
        u.realname = fake.name()
        with open('mxavatar.json','r') as f:
            avatar_list = json.load(f)
        u.avatar = choice(avatar_list)
        u.signature = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        u.gender = GenderEnum(randint(1,3))
        u.join_time = fake.date_this_year(before_today=True, after_today=False)
        u.role = role
        db.session.add(u)
        msg[r] = u.telephone
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        print('测试用户生成失败！')
        return
    print('测试用户生成成功！')
    print(msg)


def test_permission_user():
    ps=['LOGIN','VIEW_POST','PUBLISH_POST','PUBLISH_COMMENT','LOGIN_CMS','MANAGE_POST','MANAGE_COMMENTE',
        'BOARDER','BANNER','FRONTUSER','CMSUSER','ADMINER']
    msg={}
    for p in ps:
        permissions = Permission.ALL_PERMISSION-getattr(Permission,p)
        role = Role(name='FrontUser',permissions=permissions)
        u = User()
        u.telephone = fake.phone_number()
        u.username = 'NOT--'+ p
        u.email = fake.ascii_free_email()
        u.password = 'password'
        u.confirm = True
        u.realname = 'NOT-'+ p
        with open('mxavatar.json','r') as f:
            avatar_list = json.load(f)
        u.avatar = choice(avatar_list)
        u.signature = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        u.gender = GenderEnum(randint(1,4))
        u.join_time = fake.date_this_year(before_today=True, after_today=False)
        u.role = role
        db.session.add(u)
        msg[u.username] = u.telephone
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    print('测试用户生成成功！')
    print(msg)


def set_permission():

    all_users = User.query.all()
    n = 0
    for u in all_users:
        if not u.role:
            r = Role()
            u.role = r
            db.session.add(u)
            n+=1
    try:
        db.session.commit()
        print('设置成功,%d个'%n)
    except Exception:
        db.session.rollback()
        print('设置失败')

def fake_apply(p):
    types = ['top','highlight']
    for t in types:
        if not p.is_applied(t):
            a = Apply(type=t,create_time=fake.date_this_year(before_today=True, after_today=False))
            p.apply.append(a)
            db.session.add(a)



