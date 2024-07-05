import hashlib
import os
from PIL import Image
from flask_jwt_extended import create_access_token, JWTManager
from pytorch_model.image_classifier import get_imgGeneral
from pytorch_model.AipImageClassify import get_prediction
from common.md5random import sjs
from flask import Flask, jsonify, request, render_template, send_from_directory, session
from flask_cors import CORS
from common.database import init_db

app = Flask(__name__, static_url_path="/", static_folder="static", template_folder="templates")
CORS(app)  # 解决跨域问题
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wht050106@localhost:3306/sanyeqing_flask?charset=utf8'
UPLOAD_FOLDER = './static/sanyeqing_uploads/'  # 替换为实际路径
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set the secret key for JWTs
app.config['JWT_SECRET_KEY'] = 'rueqhruehurhehrui32788287'  # Change this!
jwt = JWTManager(app)
# 实例化db对象
init_db(app)


# 定义404错误页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('/error/error-404.html')


# 定义500错误页面
@app.errorhandler(500)
def serve_error(e):
    return render_template('/error/error-500.html')


'''图像分类'''


@app.route("/file", methods=['POST'])
def upfile():
    params_file = request.files['file']  # 接收文件
    dst = os.path.join(os.path.dirname(__file__), sjs() + params_file.name)  # 随机文件名
    params_file.save(dst)  # 保存文件
    cont = ""  # 文件流变量
    with open(dst, 'rb') as file:  # 读取文件
        cont = file.read()
    os.remove(dst)  # 删除文件
    type = int(request.form['type'])  # 获取表单数据type
    response = get_imgGeneral(type, cont)  # 返回识别结果
    return response


@app.route("/predict", methods=["POST"])
def predict():
    image = request.files["file"]
    img_bytes = image.read()
    info = get_prediction(image_bytes=img_bytes)
    # print(info)
    return jsonify(info)


# 保存图片
@app.route("/save", methods=["GET", "POST"])
def saveImage():
    file = request.files['file']  # 获取文件
    filename = request.form['filename']  # 获取文件名
    if not filename.endswith('.png'):  # 确保文件名以.png结尾
        filename += '.png'
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # 拼接文件路径
    # 使用Pillow打开图像并改变其尺寸
    img = Image.open(file)
    img = img.resize((300, 300))

    # 保存新的尺寸的图像
    img.save(path, 'PNG')
    # file.save(path)  # 保存文件

    return "File has been saved successfully!", 200  # 返回成功信息


@app.route('/', methods=['GET', 'POST'])
def login():
    # get直接读取填写的数据
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/qita', methods=['GET', 'POST'])
def qita():
    return render_template('qita.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.context_processor
def inject_tools_type():
    type = {
        '/person': '个人中心',
        '/photo': '我的图片',
        '/home': '我的首页'
    }
    return dict(article_type=type)


@app.template_filter('first_part')
def first_part_filter(s):
    return s.split('-')[0]


@app.template_filter('last_part')
def last_part_filter(s):
    return s.split('-')[-1]


@app.template_filter('format_date')
def format_date_filter(d, fmt):
    return d.strftime(fmt)


# 定义自定义过滤器
def my_truncate(s, length, end='...'):
    count = 0
    new_s = ''
    if len(s) <= length:
        return s
    for c in s:
        new_s += c  # 每循环一次,将一个字符添加到new_s字符串后面
        if ord(c) <= 128:  # 如果字符的ASCII码小于128,则是英文字符
            count += 1  # 英文字符占一个字符的长度
        else:
            count += 2  # 非英文字符占两个字符的长度
        if count > length:
            break
    return new_s + end


# 注册自定义过滤器
app.jinja_env.filters.update(truncate=my_truncate)


@app.route('/api/images')
def get_images():
    image_folder = os.path.join(app.root_path, 'static/sanyeqing_uploads')
    images = os.listdir(image_folder)
    return jsonify(images)


@app.route('/api/images/<filename>')
def get_image(filename):
    image_folder = os.path.join(app.root_path, 'static/sanyeqing_uploads')
    return send_from_directory(image_folder, filename)

