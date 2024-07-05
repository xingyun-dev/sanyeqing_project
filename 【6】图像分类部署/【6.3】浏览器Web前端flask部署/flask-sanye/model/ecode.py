from sqlalchemy import Table
from common.database import db
from app import app

# 创建上下文
with app.app_context():
    class Ecode(db.Model):
        __table__ = Table('ecode', db.metadata, autoload_with=db.engine)

        #插入邮箱和ecode
        def insert_ecode(self,email,code):
            ecode = Ecode(email=email,code=code)
            db.session.add(ecode)
            db.session.commit()
            return ecode

        #验证验证码
        def check_ecode(self, email, ecode):
            # 查询数据库，查找邮件和验证码
            record = db.session.query(Ecode).filter_by(email=email).first()
            if record is None or record.code != ecode:
                # 如果没有找到记录或者验证码不正确，返回False
                return False
            # 如果验证码正确，删除它然后返回True
            db.session.delete(record)
            db.session.commit()
            return True
