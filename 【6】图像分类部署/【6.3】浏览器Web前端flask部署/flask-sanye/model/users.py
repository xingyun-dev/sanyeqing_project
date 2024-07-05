import random
import time
from sqlalchemy import Table, func
from common.database import db
from app import app

# 创建上下文
with app.app_context():
    class Users(db.Model):
        __table__ = Table('users', db.metadata, autoload_with=db.engine)

        # 查询用户名,可用于注册时判断用户名是否已注册,也可用于登录校验
        def find_by_username(self, username):
            result = db.session.query(Users).filter_by(username=username).all()
            return result

        # 实现注册,首先注册时用户只需要输入用户名和密码即可,所以只需要两个参数
        # 注册时,在模型类中为其它字段尽力生成一些可用的值式,虽不全面,但是可用
        # 通常用户注册时不建议填写太多资料,影响体验,可待用户后续逐步完善
        def do_register(self, username, password):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
            avatar = str(random.randint(1, 22))  # 从22张头像图片中随机选择一张头像
            user = Users(username=username, password=password, nickname=nickname, avatar=avatar + '.png', role='user',
                         createtime=now, updatetime=now)
            db.session.add(user)
            db.session.commit()
            return user

        # def do_ecode(self,ecode):
        #

        # 实现找回密码
        def do_reset(self, username, newpass):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            user = Users.query.filter_by(username=username).first()
            if user:
                user.password = newpass
                user.updatetime = now
                db.session.commit()
                return user
            else:
                return None

        # 根据用户id查询用户信息
        def find_by_userid(self, userid):
            result = db.session.query(Users).filter_by(userid=userid).first()
            return result

        # 查询所有的用户
        def find_all_users(self, start, count):
            result = db.session.query(Users).order_by(Users.userid.desc()).limit(count).offset(
                start).all()
            return result

        def find_all_users_all(self):

            result = db.session.query(Users).all()
            return result

        def find_all_users_nickname(self):

            result = db.session.query(Users.nickname).all()
            return result

        # 根据昵称查询用户id
        def find_userid_by_nickname(self, nickname):
            result = db.session.query(Users.userid).filter_by(nickname=nickname).first()
            return result

        # 查询身份为admin的用户
        def find_by_admin(self):
            result = db.session.query(Users).filter_by(role="admin").first()
            return result

        # 查询用户的总数量
        def get_count_all_user(self):
            result = db.session.query(Users).count()
            return result

        # 按照用户昵称模糊查询
        def find_by_mingzi(self, nickname):
            result = db.session.query(Users).filter(
                Users.nickname.like('%' + nickname + '%')
            ).order_by(Users.userid.desc()).all()
            return result

        # 根据用户id删除用户
        def delete_by_user_id(self, user_id):
            user = db.session.query(Users).filter(Users.userid == user_id).first()
            if user:
                # 找到对应的用户
                db.session.delete(user)
                db.session.commit()
                return True
            else:
                # 未找到对应的用户
                return False

        # 更新用户设置信息
        def update_user(self, userid, nickname, avatar, introduce):
            user_information = db.session.query(Users).filter_by(userid=userid).first()
            if nickname:
                user_information.nickname = nickname
            if avatar:
                user_information.avatar = avatar
            if introduce:
                user_information.introduce = introduce
            db.session.commit()

        # 随机查询用户
        def find_random_users(self, num):
            # 随机查询用户
            random_users = db.session.query(Users).order_by(func.random()).limit(num).all()
            return random_users
