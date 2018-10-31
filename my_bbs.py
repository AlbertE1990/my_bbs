import click
from apps import create_app
from flask_migrate import Migrate,MigrateCommand
from exts import db
from apps.models import PostModel,CommentModel,User,Role,Permission,Group,Apply
import fake_
import test


app = create_app()
Migrate(app,db)


@app.shell_context_processor
def make_shell_context():
    context = dict(app=app,
                   db=db,
                   PostModel=PostModel,
                   CommentModel=CommentModel,
                   User = User,
                   Role = Role,
                   Permission = Permission,
                   Group = Group,
                   Apply = Apply
                   )
    return context


@app.cli.command()
def comments():
    fake_.comments()


@app.cli.command()
@click.option('--count')
def posts(count):
    count = int(count)
    fake_.posts(count)


@app.cli.command()
@click.option('--count')
def boards(count):
    count = int(count)
    fake_.boards(count)

@app.cli.command()
def frontuser():
    fake_.front_user()


@app.cli.command()
def test_group_user():
    fake_.test_group_user()


@app.cli.command()
def test_permission_user():
    fake_.test_permission_user()

@app.cli.command()
def set_permission():
    fake_.set_permission()

@app.cli.command()
def reset_permission():
    for u in User.query.all():
        group = u.role.group
        u.role.permissions = sum(group.value)
        db.session.add(u)
    db.session.commit()

@app.cli.command()
def gen_apply():
    posts = PostModel.query.all()
    for p in posts:
        fake_.fake_apply(p)
    db.session.commit()
    print('生成成功！')
