from flask import Blueprint, render_template
from model.photos import Photos
from model.users import Users
person = Blueprint('person', __name__)


# 个人中心的首页
@person.route("/person/<int:userid>")
def index(userid):
    photo = Photos()
    photo_user_count = photo.get_count_user_photos(userid)
    photo_count = photo.get_photos_count()
    user_at = Users().find_by_userid(userid)
    user_count = Users().get_count_all_user()
    return render_template("/shujumianbang/index.html",photo_user_count=photo_user_count
                           , photo_count=photo_count,
                           user_at=user_at,  userid=userid,user_count=user_count)
