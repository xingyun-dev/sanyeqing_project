import hashlib
import os
import re
from flask import Blueprint, make_response, session, request, jsonify
from common.utility import imagecode, gen_email_code, send_email
from model.users import Users
from model.ecode import Ecode

user = Blueprint('user', __name__)

font_dir = 'common'  # 字体文件所在的目录
font_filename = 'Arial.ttf'  # 字体文件名
font_path = os.path.join(font_dir, font_filename)  # 构建完整路径


@user.route('/vcode')
def vcode():
    bstring, code = imagecode(font_path=font_path).get_code()
    response = make_response(bstring)
    response.headers['content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response


@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    if not re.match(r'.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code  # 保存邮箱验证码到session中
        return 'send-pass'
    except:
        return 'send-fail'


@user.route('/user', methods=['POST'])
def register():
    users = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()

    # 校验邮箱验证码是否正确
    if ecode != session.get('ecode'):
        return 'ecode-error'
    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'

    # 验证用户名是否已经存在
    elif len(users.find_by_username(username)) > 0:
        return 'username-exist'

    else:
        # 实现注册功能
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        result = users.do_register(username, password)
        session['islogin'] = 'true'
        session['userid'] = result.userid
        session['username'] = result.username
        session['nickname'] = result.nickname
        session['role'] = result.role

        return 'reg-pass'


@user.route('/reset', methods=['POST'])
def reset():
    users = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').strip()

    # 校验邮箱验证码是否正确
    if ecode != session.get('ecode'):
        return 'ecode-error'
    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return 'up-invalid'
    else:
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        user = users.do_reset(username, password)  # 调用密码重置方法
        if user:
            # 密码重置成功
            return 'reset-pass'
        else:
            # 用户不存在，密码重置失败
            return 'user-not-found'


@user.route('/login', methods=['POST'])
def login():
    users = Users()
    # latitude = request.form.get('latitude').strip()
    # longitude = request.form.get('longitude').strip()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()  # 图形验证码

    # 校验图形验证码是否正确
    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'
    else:
        # 实现登录功能
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        result = users.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = result[0].username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role

            # 将cookie写入浏览器
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
            response.set_cookie('password', password, max_age=7 * 24 * 3600)
            print('dkfjhs')
            return response

        else:
            return 'login-fail'


@user.route('/ecode_wx', methods=['POST'])
def ecode_wx():
    ecode_email = Ecode()
    data = request.get_json()
    email = data.get('email')
    if not re.match(r'.+@.+\..+', email):
        return jsonify({"msg": "Invalid email address"}), 400
    code = gen_email_code()
    try:
        send_email(email, code)
        ecode_email.insert_ecode(email=email, code=code)
        return jsonify({"msg": "Email sent"}), 200
    except Exception as e:
        return jsonify({"msg": "Failed to send email", "error": str(e)}), 500


from flask_jwt_extended import jwt_required, get_jwt_identity


@user.route('/user_wx', methods=['POST'])
# @jwt_required
def register_wx():
    users = Users()
    ecode_email = Ecode()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    ecode = data.get('ecode')  # 从请求中获取验证码

    # TODO: 在这里验证验证码是否正确
    if not ecode_email.check_ecode(username, ecode):
        return jsonify({"msg": "Invalid ecode"}), 400

    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        return jsonify({"msg": "Invalid username or password"}), 400

    # 验证用户名是否已经存在
    elif len(users.find_by_username(username)) > 0:
        return jsonify({"msg": "Username already exists"}), 400

    else:
        # 实现注册功能
        password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
        result = users.do_register(username, password)
        if result:
            access_token = create_access_token(identity=username)  # 创建 JWT
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Registration failed"}), 500


from flask_jwt_extended import create_access_token

@user.route('/login_wx', methods=['POST'])
def login_wx():
    users = Users()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    password = hashlib.md5(password.encode()).hexdigest()  # 密码加密
    result = users.find_by_username(username)
    if len(result) == 1 and result[0].password == password:
        access_token = create_access_token(identity=username)
        # # 获取用户信息
        # user_info = {
        #     'userid':result[0].userid,
        #     'nickname': result[0].nickname,
        #     'avatar': result[0].avatar,
        #     'createtime': result[0].createtime,
        #     'introduce': result[0].introduce
        #     # 添加你需要的其它字段
        # }
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@user.route('/get_user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    users = Users()
    # 获取保存在 access_token 中的 identity
    username = get_jwt_identity()
    result = users.find_by_username(username)
    if len(result) == 1:
        user_info = {
            'userid': result[0].userid,
            'nickname': result[0].nickname,
            'avatar': result[0].avatar,
            'username': result[0].username,
            'introduce': result[0].introduce
            # 添加你需要的其它字段
        }
        return jsonify(user_info=user_info), 200
    else:
        return jsonify({"msg": "User not found"}), 404

@user.route('/logout')
def logout():
    # 清空session,页面跳转
    session.clear()
    response = make_response('注销并进行重定向', 302)
    # response.headers['Location'] = url_for('index.home')
    response.headers['Location'] = "/"
    response.delete_cookie('username')
    response.set_cookie('password', '', max_age=0)
    return response






@user.route('/loginfo')
def loginfo():
    # 没有登录,则直接响应一个空JSON给前端,用于前端判断
    if session.get('islogin') is None:
        return jsonify(None)
    else:
        # 登录了,则响应用户信息给前端
        dict = {}
        dict['islogin'] = session.get('islogin')
        dict['userid'] = session.get('userid')
        dict['username'] = session.get('username')
        dict['nickname'] = session.get('nickname')
        dict['role'] = session.get('role')
        return jsonify(dict)


# 删除用户
@user.route('/user/delete', methods=['POST'])
def checked_article():
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        if user.role == 'user' or user.role == 'admin':
            users = Users()
            userid = int(request.form.get('userid'))
            success = users.delete_by_user_id(userid)
            if success:
                # 删除成功
                return 'delete-success'
            else:
                # 删除失败
                return 'delete-fail'
        else:
            return 'perm-denied'
