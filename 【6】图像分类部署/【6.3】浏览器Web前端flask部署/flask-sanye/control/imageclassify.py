import math

from flask import Blueprint,session, request
from model.photos import Photos

from model.users import Users

classify = Blueprint('classify', __name__)

from flask import Flask, render_template
from functools import wraps
from flask import redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def find_by_userid(userid):
    result = Users().find_by_userid(userid)
    return result


# 图片识别
@classify.route('/classify')
def image_classify():
    return render_template('/image_classify/photo_classify.html')


# 批量处理
@classify.route('/classify_pili')
def image_classify_piliang():
    return render_template('/image_classify/photo_classify_piliang.html')


# 为系统管理首页填充图片列表,并绘制分页栏
@classify.route('/admin')
@admin_required
def sys_admin():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    photo = Photos()
    result = photo.find_all_photos(0, pagesize)
    total = math.ceil(photo.get_photos_count() / pagesize)
    return render_template('/image_classify/system-admin.html', page=1, result=result, total=total, userid=userid,
                           avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)


# 为系统管理首页的图片列表进行分页查询
@classify.route("/admin/photo/<int:page>")
@admin_required
def admin_photos(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    photo = Photos()
    result = photo.find_all_photos(start, pagesize)
    total = math.ceil(photo.get_photos_count() / pagesize)
    return render_template('/image_classify/system-admin.html', page=page, result=result, total=total, userid=userid,
                           avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)


# 按工具进行分类搜索的后台接口
@classify.route("/admin/type/<int:type>--<int:page>")
@admin_required
def admin_search_photos_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    photos = Photos()
    result, total = photos.find_by_type_photos(start, pagesize, type)
    total = math.ceil(total / pagesize)
    return render_template('/image_classify/system-admin.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)


# 为系统管理首页填充用户列表,并绘制分页栏
@classify.route("/admin-user")
@admin_required
def sys_admin_user():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    user = Users()
    result = user.find_all_users(0, pagesize)
    total = math.ceil(user.get_count_all_user() / pagesize)
    return render_template('/image_classify/system-admin-user.html', page=1, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname)


# 为系统管理首页的用户列表进行分页查询
@classify.route("/admin-user/<int:page>")
@admin_required
def admin_user(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    user = Users()
    result = user.find_all_users(start, pagesize)
    total = math.ceil(user.get_count_all_user() / pagesize)
    return render_template('/image_classify/system-admin-user.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname)


# 按照作者昵称进行模糊查询的后台接口
@classify.route("/admin-user/search_mingzi/<keyword>")
@admin_required
def admin_user_mingzi(keyword):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    result = Users().find_by_mingzi(keyword)
    return render_template('/image_classify/system-admin-user.html', page=1, result=result, total=1, userid=userid,
                           avatar=avatar, nickname=nickname)


# 我的图片
@classify.route('/ucenter')
def ucenter_article():
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    photos = Photos()
    user_id = session.get('userid')
    result = photos.user_query_photos_page(user_id, 0, pagesize)
    total = math.ceil(photos.get_count_user_photos(user_id) / pagesize)
    return render_template('/image_classify/user-center.html', page=1, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)


# 为我的文章页面的文章列表进行分页查询
@classify.route("/ucenter/<int:page>")
def ucenter_photo_page(page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    user_id = session.get('userid')
    photos = Photos()
    result = photos.user_query_photos_page(user_id, start, pagesize)
    total = math.ceil(photos.get_count_user_photos(user_id) / pagesize)
    return render_template('/image_classify/user-center.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)


# 按我的图片进行分类搜索的后台接口
@classify.route("/ucenter/type/<int:type>--<int:page>")
def user_search_type(type, page):
    userid = session.get('userid')
    avatar = session.get('avatar')
    nickname = session.get('nickname')
    pagesize = 50
    start = (page - 1) * pagesize
    photos = Photos()
    result, total = photos.find_by_type_photos_userid(start, pagesize, type, userid)
    total = math.ceil(total / pagesize)
    return render_template('/image_classify/user-center.html', page=page, result=result, total=total,
                           userid=userid, avatar=avatar, nickname=nickname, find_by_userid=find_by_userid)
