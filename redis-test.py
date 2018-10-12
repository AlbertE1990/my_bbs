from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()


class Permission():

    #1.前端登录
    LOGIN                       = 0b1
    #2.查看帖子
    VIEW_POST                   = 0b10
    #3.发表帖子
    PUBLISH_POST                = 0b100
    #4.发表评论
    PUBLISH_COMMENT             = 0b1000
    #5.后台登录
    LOGIN_CMS                   = 0b10000
    # 6.管理帖子
    MANAGE_POST                 = 0b100000
    # 7.管理评论
    MANAGE_COMMENTE             = 0b1000000
    # 8.管理前台用户账号
    MANAGE_FRONTUSER_ACCOUNT    = 0b10000000
    # 9.管理前台用户权限
    MANAGE_FRONTUSER_PERMISSION = 0b100000000
    # 10.管理板块
    BOARDER                     = 0b1000000000
    #11.管理轮播图
    BANNER                      = 0b10000000000
    #12.管理后台用户账户
    MANAGE_OPERATOR_ACCOUNT     = 0b100000000000
    #13.管理后台用户权限
    MANAGE_OPERATOR_PERMISSION  = 0b1000000000000
    #14.管理管理员账户
    MANAGE_ADMINSTRATOR_ACCOUNT = 0b10000000000000
    #15.管理管理员权限
    MANAGE_ADMINSTRATOR_PERMISSION = 0b100000000000000
    #16.超级管理员
    SU                          = 0b1000000000000000
    # 所有权限
    ALL_PERMISSION              = 0b1111111111111111


class Group(enum.Enum):
    FrontUser     = [Permission.LOGIN, Permission.VIEW_POST, Permission.PUBLISH_POST,
                     Permission.PUBLISH_COMMENT]
    Operator      = FrontUser + [Permission.LOGIN_CMS,Permission.MANAGE_POST,Permission.MANAGE_COMMENTE,
                                      Permission.MANAGE_FRONTUSER_ACCOUNT,Permission.MANAGE_FRONTUSER_PERMISSION]
    Administrator = Operator + [Permission.BANNER,Permission.BOARDER,Permission.MANAGE_OPERATOR_ACCOUNT,
                                     Permission.MANAGE_ADMINSTRATOR_PERMISSION]
    Super = [Permission.ALL_PERMISSION]


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    u_id = db.Column(db.String(100), db.ForeignKey('user.id'))
    group = db.Column(db.Enum(Group),default=Group.FrontUser,nullable=False)
    permissions = db.Column(db.Integer,nullable=False)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.group is None:
            self.group = 'FrontUser'
        if self.permissions is None:
            self.permissions = sum(getattr(Group,self.group,0).value)
        else:
            self.permissions = min(sum(getattr(Group,self.group).value),self.permissions)
