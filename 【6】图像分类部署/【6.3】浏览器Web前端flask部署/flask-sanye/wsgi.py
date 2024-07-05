from flask import send_from_directory

from app import app


@app.route('/api/images')
def get_images():
    image_folder = os.path.join(app.root_path, 'static/sanyeqing_uploads')
    images = os.listdir(image_folder)
    return jsonify(images)


@app.route("/api/images_my")
def get_images_my():
    userid = request.args.get('userid')  # 从查询参数中获取 userid
    if userid is None:
        return jsonify({"error": "Missing userid parameter"}), 400  # 如果没有 userid，返回错误
    images = Photos().user_query_photos(user_id=userid)  # 查询所有图片
    image_data = [{"photos_name": image.photos_name, "photos_type": image.photos_type} for image in images]
    return jsonify(image_data)


@app.route('/api/images/<filename>')
def get_image(filename):
    image_folder = os.path.join(app.root_path, 'static/sanyeqing_uploads')
    return send_from_directory(image_folder, filename)


@app.route('/api/avatar/<avatar>')
def get_avatar(avatar):
    image_folder = os.path.join(app.root_path, 'static/chat_room/images')
    return send_from_directory(image_folder, avatar)




# 定义全局拦截器,实现自动登录
@app.before_request
def before():
    url = request.url
    pass_list = ['/login', '/user', '/logout']
    if url in pass_list or url.endswith('.js') or url.endswith('.css1') or url.endswith('.jpg'):
        pass

    if session.get('islogin') is None:
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if username is not None and password is not None:
            users = Users()
            result = users.find_by_username(username)
            if len(result) == 1 and result[0].password == password:
                session['islogin'] = 'true'
                session['userid'] = result[0].userid
                session['username'] = result[0].username
                session['nickname'] = result[0].nickname
                session['role'] = result[0].role
                session['avatar'] = result[0].avatar
#
#
# @app.route('/login_wx', methods=['POST'])
# def login_wx():
#     users = Users()
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#
#     password = hashlib.md5(password.encode()).hexdigest()
#     result = users.find_by_username(username)
#
#     if len(result) == 1 and result[0].password == password:
#         access_token = create_access_token(identity=username)
#         return jsonify(access_token=access_token), 200
#
#     else:
#         return jsonify({"msg": "login-fail"}), 401
#



from control.user import *

app.register_blueprint(user)
from control.home import *

app.register_blueprint(home)
from control.person import *
app.register_blueprint(person)
from control.photo import *

app.register_blueprint(photo)
from control.imageclassify import *

app.register_blueprint(classify)


app.run()