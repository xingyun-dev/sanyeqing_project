import base64
import io
import os
import time

from PIL import Image
from flask import Blueprint ,session, request
from common.utility import compress_image

from model.users import Users
from model.photos import Photos

photo = Blueprint('photo', __name__)

from flask import Flask, render_template


# 根据photos_type查询photos表中二级分类信息
def get_photos_by_type(type):
    tools = Photos()
    result = tools.get_photos_message_by_type(type)
    return result


# 根据photos_type查询photos表中一级分类信息
def get_photos_by_majortype(majortype):
    tools = Photos()
    result = tools.get_photos_message_by_major_category(majortype)
    return result


# 根据photos_type命名对应的分类信息
from common.utility import ming_photos_by_type


# 图片库
@photo.route('/photo', methods=['GET', 'POST'])
def photo_ku():
    userid = session.get('userid')
    user_all_photos = Photos().user_query_photos(user_id=userid)
    all_photos = Photos().get_photos_message()
    return render_template('/photo_chuli/photo_view.html', get_photos_by_type=get_photos_by_type,
                           get_photos_by_majortype=get_photos_by_majortype, ming_photos_by_type=ming_photos_by_type,
                           all_photos=all_photos, user_all_photos=user_all_photos)


# 个人图片
@photo.route('/photo/<int:userid>')
def person_photo(userid):
    user_all_photos = Photos().user_query_photos(user_id=userid)
    all_photos = Photos().get_photos_message()
    user_one = Users().find_by_userid(userid=userid)
    return render_template('/photo_chuli/photo_view.html', userid=userid, user_one=user_one,
                           get_photos_by_type=get_photos_by_type,
                           get_photos_by_majortype=get_photos_by_majortype, ming_photos_by_type=ming_photos_by_type,
                           all_photos=all_photos, user_all_photos=user_all_photos)


# 工具二级分类后的大页面接口
@photo.route('/photos/type/<int:type>', methods=['GET', 'POST'])
def tools_type(type):
    return render_template('/photo_chuli/fenlei.html', type=str(type), ming_photos_by_type=ming_photos_by_type,
                           get_photos_by_type=get_photos_by_type, get_photos_by_majortype=get_photos_by_majortype)


# 工具二级分类后的大页面接口
@photo.route('/photos/type/<int:userid>--<int:type>', methods=['GET', 'POST'])
def tools_type_user(userid, type):
    user_one = Users().find_by_userid(userid=userid)
    return render_template('/photo_chuli/fenlei.html', type=str(type), ming_photos_by_type=ming_photos_by_type,
                           get_photos_by_type=get_photos_by_type, get_photos_by_majortype=get_photos_by_majortype,
                           user_one=user_one)


# 新建图片接口
@photo.route('/insert_photos', methods=['POST'])
def insert_photos():
    photos_name = request.form.get('photos_name')
    photos_type = request.form.get('photos_type')
    predict = request.form.get('predict')
    photos_userid = session.get('userid')

    if session.get('userid') is None:
        return 'perm-denied'
    else:
        # 解码 base64 字符串
        data_url = photos_name
        decoded_bytes = base64.b64decode(data_url)
        image_stream = io.BytesIO(decoded_bytes)

        # 打开图片
        image = Image.open(image_stream)
        thumbname = time.strftime(predict + "-%Y%m%d_%H%M%S-" + str(session.get('nickname')) + ".png")
        # 保存缩略图到文件
        image.save('./static/sanyeqing_uploads/' + thumbname, format='png')
        compress_image('./static/sanyeqing_uploads/' + thumbname, './static/sanyeqing_uploads/' + thumbname, 300)
        # 去掉后缀
        photos_name = os.path.splitext(thumbname)[0]
        photos = Photos()
        try:
            photos.insert_photos_message(photos_name=photos_name,
                                         photos_type=photos_type,
                                         photos_userid=photos_userid,
                                         )
            return 'add-pass'
        except:
            return 'add-fail'

# 删除图片信息
@photo.route('/photos/delete', methods=['POST'])
def delete_photos():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        photos_id = int(request.form.get('photos_id'))
        success = Photos().delete_photos_message(photos_id)
        if success:
            # 删除成功
            return 'delete-success'
        else:
            # 删除失败
            return 'delete-fail'



# 隐藏文章
@photo.route('/photos/hidden', methods=['POST'])
def hidden_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or 'admin':
            photos_id = int(request.form.get('photos_id'))
            success = Photos().switch_hide(photos_id)
            if success == 1:
                # 隐藏成功
                return 'hidden-success'
            elif success == 0:
                # 取消隐藏
                return 'hidden-cancel'
        else:
            return 'perm-denied'



# #审核工具接口
# @tools.route('/tools/checked', methods=['POST'])
# def checked_article():
#     if session.get('userid') is None:
#         return 'perm-denied'
#     else:
#         user = Users().find_by_userid(session.get('userid'))
#         if user.role == 'user' or 'admin':
#             tools_id = int(request.form.get('tools_id'))
#             tools = Tools()
#             success = tools.switch_checked(tools_id=tools_id)
#             if success == 1:
#                 # 已经审核
#                 return 'checked-success'
#             elif success == 0:
#                 # 还未审核
#                 return 'checked-cancel'
#         else:
#             return 'perm-denied'
