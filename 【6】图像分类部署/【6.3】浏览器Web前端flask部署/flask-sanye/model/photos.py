import time

from common.database import db
from app import app
from model.users import Users

from sqlalchemy import Table

# 创建上下文
with ((app.app_context())):
    class Photos(db.Model):
        __table__ = Table('photos', db.metadata, autoload_with=db.engine)

        # 1代表三叶青块根照片,
        # 2代表三叶青叶片照片，
        # 3代表其它,

        # 根据photo_type查询photos表中信息
        def get_photos_message_by_type(self, photos_type):
            result = db.session.query(Photos).filter(Photos.photos_type == photos_type, Photos.photos_hide == 0).all()
            return result

        # 查询某一大类下的所有图片，使用startswith和%通配符

        def get_photos_message_by_major_category(self, major_category):
            result = db.session.query(Photos).filter(Photos.photos_type.startswith(major_category),
                                                     Photos.photos_hide == 0).all()
            return result

        # 查询所有图片
        def get_photos_message(self):
            result = db.session.query(Photos).filter(Photos.photos_hide == 0).all()
            return result


        # 查询所有图片数量
        def get_photos_count(self):
            count = db.session.query(Photos).filter(Photos.photos_hide == 0).count()
            return count

        # # 根据photos_id查询图片的信息
        # def get_photos_message_by_id(self, photos_id):
        #     result = db.session.query(Photos).filter(Photos.photos_id == photos_id, Photos.photos_hide == 0).first()
        #     return result
        #
        # # 根据工具的分类随机查询6条工具信息（充当相关导航）
        # def get_tools_random_6_by_type(self, tools_type):
        #     # 首先根据工具类型筛选工具
        #     filtered_tools = self.get_tools_message_by_type(tools_type)
        #     # 如果没有找到该类型的工具，返回空列表
        #     if not filtered_tools:
        #         return []
        #         # 从筛选后的工具中随机选择6条
        #     random_tools = random.sample(filtered_tools, min(6, len(filtered_tools)))
        #
        #     return random_tools

        # 插入图片信息

        def insert_photos_message(self, photos_userid, photos_type, photos_name, photos_hide=0):
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            photos = Photos(photos_userid=photos_userid, photos_type=photos_type, photos_hide=photos_hide,
                            photos_name=photos_name, createtime=now)
            db.session.add(photos)
            db.session.commit()

        # 删除图片信息
        def delete_photos_message(self, photos_id):
            photos = db.session.query(Photos).filter(Photos.photos_id == photos_id).first()
            if photos:
                # 找到对应的编辑设置信息
                db.session.delete(photos)
                db.session.commit()
                return True
            else:
                # 未找到
                return False

        # 切换文章的隐藏状态：1表示隐藏,0表示显示
        def switch_hide(self, photos_id):
            row = db.session.query(Photos).filter_by(photos_id=photos_id).first()
            if row.photos_hide == 1:
                row.photos_hide = 0
            else:
                row.photos_hide = 1
            db.session.commit()
            return row.photos_hide  # 将当前最新状态返回给控制层

        # # 审核提交的工具提交信息
        #
        # def switch_checked(self, tools_id):
        #     row = db.session.query(Tools).filter_by(tools_id=tools_id).first()
        #     if row.tools_check == 0:
        #         row.tools_check = 1
        #     else:
        #         row.tools_check = 0
        #     db.session.commit()
        #     return row.tools_check  # 将当前最新状态返回给控制层

        # 根据某个指定用户查询其下所有提交的图片
        def user_query_photos(self, user_id):
            result = db.session.query(Photos).join(Users, Users.userid == Photos.photos_userid).filter(
                Users.userid == user_id, Photos.photos_hide == 0  # 添加一个条件来指定要查询的用户ID
            ).all()
            return result

        def user_query_photos_page(self, user_id, start, count):
            result = db.session.query(Photos).join(Users, Users.userid == Photos.photos_userid).filter(
                Users.userid == user_id,  # 添加一个条件来指定要查询的用户ID
            ).order_by(Photos.photos_id.desc()).limit(count).offset(
                start).all()
            return result

        # 根据某个指定用户查询其下所有提交图片的数量 (已经通过审核)
        def get_count_user_photos(self, user_id):
            result = db.session.query(Photos, Users).join(Users, Users.userid == Photos.photos_userid).filter(
                Users.userid == user_id, Photos.photos_hide == 0  # 添加一个条件来指定要查询的用户ID
            ).count()
            return result

            # 查询photos表中的所有数据并返回结果集

        def find_all_photos(self, start, count):
            result = db.session.query(Photos).join(Users, Users.userid == Photos.photos_userid).order_by(
                Photos.photos_id.desc()).limit(count).offset(
                start).all()
            return result

        # 按照工具分类进行查询(该方法直接返回工具总数量用于分页)
        def find_by_type_photos(self, start, count, category):
            if category == 0:
                result = self.find_all_photos(start, count)
                total = self.get_photos_count()
            else:
                result = db.session.query(Photos).join(Users,
                                                       Users.userid == Photos.photos_userid).filter(
                    Photos.photos_type == category).order_by(
                    Photos.photos_id.desc()).limit(count).offset(start).all()

                total = db.session.query(Photos).filter(Photos.photos_type == category).count()
            return result, total  # 返回分页结果集和不分页的总数量

        def find_by_type_photos_userid(self, start, count, category, userid):
            if category == 0:
                result = self.user_query_photos_page(start, count, userid)
                total = self.get_count_user_photos(userid)
            else:
                result = db.session.query(Photos).join(Users,
                                                       Users.userid == Photos.photos_userid).filter(
                    Photos.photos_type == category, Photos.photos_userid ==
                    userid).order_by(
                    Photos.photos_id.desc()).limit(count).offset(start).all()
                total = db.session.query(Photos).filter(Photos.photos_type == category, Photos.photos_userid == userid
                                                        ).count()
            return result, total  # 返回分页结果集和不分页的总数量
