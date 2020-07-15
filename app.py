# -*- coding: <utf-8> -*-
import sys
sys.path.append('/home/ubuntu/learningweb')
import hashlib
from datetime import timedelta

import pymysql
from flask import *
from flask_sqlalchemy import SQLAlchemy
from models import *
app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8" #指定浏览器渲染的文件类型，和解码格式；
# class Config(object):
#     SECRET_KEY = "DJFAJLAJAFKLJQ"
#
# app.config.from_object(Config())
#设置session
app.config['SECRET_KEY']="Learn Python hahaha"
##############################################################
###############------数据库连接关闭函数------##################
##############################################################
# 创造你的数据库引擎
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@127.0.0.1:3306/learningweb_db?charset=utf8mb4"
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db.init_app(app)
db_session = db.session
#######################################################################################
# # 连接数据库
# def connectdb():
#     db = pymysql.connect(HOST, USER, PASSWORD, DATABASE, charset='utf8')
#     db.autocommit(True)
#     cursor = db.cursor()
#     return (db,cursor)
#
# # 关闭数据库
# def closedb(db,cursor):
#     db.close()
#     cursor.close()
##############################################################
#######------------登录状态session校验-----------##############
##############################################################
def login_check(func):
    def inner(*args,**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return func(*args,**kwargs)
    return inner
##############################################################
###############------------首页-----------####################
##############################################################
#首页
@app.route('/')
def index():
    return render_template('index.html')
#其他页面点击首页，触发url执行该视图函数
@app.route('/<username>' ,methods=['GET'])
def to_index(username):
    if session.get('user_id'):
        # 查询数据
        user_info_data = User.query.filter_by(username=username).first()
        # print(user_info_data)     #(1, '18768486601', 'zzj', 'zzj123')
        user_info = {
            'user_id':user_info_data.user_id,
            'phone':user_info_data.phone,
            'username':user_info_data.username,
            'password':user_info_data.password
        }
        print(user_info)    # {'user_id': 1, 'phone': '18768486601', 'username': 'zzj', 'password': 'zzj123'}
        print(type(user_info))  #  <class 'dict'>

        # 设置session---并且设置有效期
        # session['user_id'] = user_info['user_id']
        # session.permanent = True
        # app.permanent_session_lifetime = timedelta(minutes=30)

        return render_template('index2.html',user = user_info)
    else:
        return redirect(url_for('login'))
##############################################################
##############注册----(GET访问注册页面；POST表单处理)###########
##############################################################
@app.route('/user_regist', methods=['GET'])
def regist():
    return render_template('regist.html')

@app.route('/user_regist', methods=['POST'])
def user_regist():

    # try:
    # 获取post数据
    # phone = request.form['phone']
    # username = request.form['username']
    # password = request.form['password']
    phone = request.get_json()['phone']
    username = request.get_json()['username']
    password = request.get_json()['password']
    #检测手机号是否被注册
    check_phone = User.query.filter_by(phone=phone).first()
    # 检测用户名是否被注册
    check_username = User.query.filter_by(username=username).first()
    if check_phone or check_username :
        if check_phone:
            return jsonify({'status':500,'msg':'手机号已经被注册！'})
        elif check_username:
            return jsonify({'status':500,'msg':'用户名已经被注册！'})
        # return '注册信息不符合规范或填写信息已被注册！'
        # return False
    else:
        # 添加数据

        ##对密码进行加密，再存入数据库
        #pm = hashlib.md5()
        #pm.update(password.encode())
        add_user = User(phone=phone,username=username,password=password)
        db_session.add(add_user)
        db_session.commit()
        # l = [phone, username, password]
        # ins = "insert into user_info(phone, username, password) values(%s, %s, %s)"
        # cursor.execute(ins, l)
        # 最后添加行的id
        # user_id = cursor.lastrowid

    # except Exception as e:
    #     print(e)
    #     return jsonify({'msg':'注册信息不符合规范或填写信息已被注册！'})

    # return redirect(url_for('login'))
    return jsonify({'status':200,'msg':'注册成功！'})
##############################################################
############### 登录（GET访问登录页面；POST表单处理）###########
#############################################################
@app.route('/user_login', methods=['GET'])
def login():
    return render_template('login.html')
@app.route('/user_login', methods=['POST'])
def user_login():

    # try:

    # 获取post数据  审核数据
    # phone = request.form['phone']
    # password = request.form['password']
    phone = request.get_json()['phone']
    password = request.get_json()['password']
    print(phone)
    print(password)
    

    check_phone = User.query.filter_by(phone=phone).first()
    if check_phone:
        check_pwd = User.query.filter_by(password=password).first()
        if not check_pwd:
            msg = {'status':500,'msg': '用户名或密码错误!'}
            return jsonify(msg)
            # return render_template('login.html')
    else:
        msg = {'status':500,'msg':'用户名或密码错误!'}
        return jsonify(msg)
        # return render_template('login.html')

    # 获取行的id
    print(check_pwd)   # (1, '18768486601', 'zzj', 'zzj123')
    print(type(check_pwd))  #<class 'tuple'>
    username = check_phone.username

    #设置session---并且设置有效期
    session['user_id'] = check_phone.user_id
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

    # except Exception as e:
    #     print(e)
    #     msg = {'status':500,'msg': '服务器错误!'}
    #     return jsonify(msg)


    # print(user_id)      # 1
    # print(type(user_id))  # <class 'int'>

    # return redirect(url_for('login_success', username=username))
    return jsonify({'status':200,'msg':'登录成功！','username':username})

#登录成功，跳转至首页显示欢迎XXX用户
#-------------------------------------------------用户登录状态需要检测-----否则输入该地址直接就可以访问登录成功后的状态页面了。



##############################################################
################# 图书页面（GET访问图书页面）##################
#############################################################
@app.route('/<username>/book', methods=['GET'],endpoint='book')
@login_check
def book(username):
    return render_template('test_book.html',username =username)

@app.route('/<username>/book', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_book(username):
    # username = request.args.get('username',type=str)
    # page = request.args.get('page')      #############args只获取地址栏中参数 ，不分get请求方式还是post请求方式.

    # page = request.data                       #     b'{"page":2}'     需要page.decode()  -->   str:  {"page":2}
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    url = request.path
    url1 = request.full_path
    print(url)
    # print(url1)
    # page = int(page)

    # user_info = User.query.filter_by(username=username).first()
    # print(user_info)                 # <User 1>
    # print(user_info.phone)           #  18768486601

    try:
        pagination = Book.query.order_by(Book.title.desc()).paginate(page, per_page=8)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        # print(pagination)
        # print(type(pagination))
        # print(news_list)
        # obj = pagination.query.all()
        # obj = news_list[0].title
        # print(obj)
        # user_info = User.query.filter_by(phone='18768486601').first()
        # print(user_info)
        # print(user_info.username)
        book_list = []
        for book in news_list:
            if book.img_url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['img_url']=book.img_url
                dict01['title']=book.title
                dict01['book_url']=book.book_url
                # print(dict01)
                book_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        return jsonify({'book_list': book_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})
    # print(book_list)
    # return render_template('test_book.html', pagination=pagination, news_list=news_list)
    # return jsonify({'book_list':book_list})

##############################################################
############### 博客页面（GET访问多种类型的博客页面）###########
#############################################################
#思路一： 从前端直接写要访问的url地址，通过调用前端传过来的地址参数，调取相应数据响应   \/
#思路二： 前端通过ajax发送get请求传递data信息，后端通过request.args获取前端要传递过来的页面数据，然后调取相应数据响应
#####--------------------------------------CSS_Blog-----------------------------------------------------#######
@app.route('/<username>/css', methods=['GET'],endpoint='css')
@login_check
def css_blog(username):
    pagination = CSS_Blog.query.order_by(CSS_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html',username=username,blog_list =blog_list)

@app.route('/<username>/css', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_css_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = CSS_Blog.query.order_by(CSS_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------JS_Blog-----------------------------------------------------#######
@app.route('/<username>/js', methods=['GET'],endpoint='js')
@login_check
def js_blog(username):
    pagination = JS_Blog.query.order_by(JS_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html',username=username,blog_list =blog_list)

@app.route('/<username>/js', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_js_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = JS_Blog.query.order_by(JS_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Vue_Blog-----------------------------------------------------#######
@app.route('/<username>/vue', methods=['GET'],endpoint='vue')
@login_check
def vue_blog(username):
    pagination = Vue_Blog.query.order_by(Vue_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/vue', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_vue_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = Vue_Blog.query.order_by(Vue_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------React_Blog-----------------------------------------------------#######
@app.route('/<username>/react', methods=['GET'],endpoint='react')
@login_check
def react_blog(username):
    pagination = React_Blog.query.order_by(React_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/react', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_react_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = React_Blog.query.order_by(React_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Python_Base_Blog-----------------------------------------------------#######
@app.route('/<username>/python_base', methods=['GET'],endpoint='python_base')
@login_check
def python_base_blog(username):
    pagination = Python_Base_Blog.query.order_by(Python_Base_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/python_base', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_python_base_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = Python_Base_Blog.query.order_by(Python_Base_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Spider_Blog-----------------------------------------------------#######
@app.route('/<username>/spider', methods=['GET'],endpoint='spider')
@login_check
def spider_blog(username):
    pagination = Spider_Blog.query.order_by(Spider_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html',username=username, blog_list=blog_list)

@app.route('/<username>/spider', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_spider_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = Spider_Blog.query.order_by(Spider_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Flask_Blog-----------------------------------------------------#######
@app.route('/<username>/flask', methods=['GET'],endpoint='flask')
@login_check
def flask_blog(username):
    pagination = Flask_Blog.query.order_by(Flask_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html',username=username, blog_list=blog_list)

@app.route('/<username>/flask', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_flask_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = Flask_Blog.query.order_by(Flask_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Machine_learning_Blog-----------------------------------------------------#######
@app.route('/<username>/machine_learning', methods=['GET'],endpoint='machine_learning')
@login_check
def ai_blog(username):
    pagination = AI_Blog.query.order_by(AI_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/machine_learning', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_ai_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = AI_Blog.query.order_by(AI_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------MySQL_Blog-----------------------------------------------------#######
@app.route('/<username>/mysql', methods=['GET'],endpoint='mysql')
@login_check
def mysql_blog(username):
    pagination = MySQL_Blog.query.order_by(MySQL_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/mysql', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_mysql_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = MySQL_Blog.query.order_by(MySQL_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})

#####--------------------------------------Redis_Blog-----------------------------------------------------#######
@app.route('/<username>/redis', methods=['GET'],endpoint='redis')
@login_check
def redis_blog(username):
    pagination = Redis_Blog.query.order_by(Redis_Blog.title.desc()).paginate(1, per_page=6)
    news_list = pagination.items
    blog_list = []
    # print(pagination)
    # print(news_list)
    for blog in news_list:
        if blog.url is not None:
            # anews.img_url = anews.img_url.split('\r\n')[0]
            dict01 = {}
            dict01['url'] = blog.url
            dict01['title'] = blog.title
            dict01['detail_info'] = blog.detail_info
            # print(dict01)
            blog_list.append(dict01)  # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
    # print(blog_list)

    return render_template('topic.html', username=username,blog_list=blog_list)

@app.route('/<username>/redis', methods=['POST'])       #   "GET /zzj/book?page=2 HTTP/1.1"   404 -
def add_redis_blog(username):
    page = request.get_json()['page']        #    能取出前端传递过来的json格式的字符串，通过字典的形式获取到里面的值   int类型也可以
    print(page)
    # print(type(page))

    try:
        pagination = Redis_Blog.query.order_by(Redis_Blog.title.desc()).paginate(page, per_page=4)  #page:指定从第几页开始    per_page : 每一页有几项
        news_list = pagination.items
        blog_list = []
        # print(pagination)
        # print(news_list)
        for blog in news_list:
            if blog.url is not None:
                # anews.img_url = anews.img_url.split('\r\n')[0]
                dict01 = {}
                dict01['url']=blog.url
                dict01['title']=blog.title
                dict01['detail_info']=blog.detail_info
                # print(dict01)
                blog_list.append(dict01)     # [{'img_url':xxx,'title':xxx,'book_url':xxx},{},{}]
        # print(blog_list)
        return jsonify({'blog_list': blog_list})
    except Exception as e:
        print(e)
        return jsonify({'error':'没有数据啦~(>_<)!!'})


##############################################################
########## 个人中心页面（GET访问个人页面，PUT更新操作）#########
#############################################################
@app.route('/<username>/myself', methods=['GET'],endpoint='myself')
@login_check
def myself(username):
    return render_template('about.html',username=username)
@app.route('/<username>/myself', methods=['POST'])
def update_myself(username):
    try:
        # 获取post数据
        # a = request.form
        # print(a)
        # data = request.data
        # print(data)
        old_password = request.get_json()['old_password']
        new_password = request.get_json()['new_password']
        # old_password = a['old_password']
        # new_password = a['new_password']
        print(old_password)
        print(new_password)


        # 连接数据库
        # (db, cursor) = connectdb()

        # 查询数据
        # cursor.execute('select * from user_info where password=%s', [old_password])
        # check_password = cursor.fetchone()
        # print(check_password)

        from models import db
        user_info = User.query.filter_by(username=username).first()
        print(user_info)                 # <User 1>
        print(user_info.password)           #  18768486601
        if user_info.password == old_password:
            #更新数据
            # db_session.commit()

            user_info.password = new_password
            print(user_info.password)

            # db_session.query(Model).filterby(password=old_password).update({'password':new_password})
            db.session.add(user_info)
            db.session.commit()
            # ins = "update user_info set password='%s' where password ='%s'"
            # cursor.execute(ins,[new_password,old_password])
            # 关闭数据库
            # closedb(db, cursor)
            return jsonify({'code':'200'})
        else:
            return jsonify({'code':'500'})
    except Exception as e:
        print(e)
        # db.rollback()
        return jsonify({'code':'500'})


if __name__ == '__main__':
    app.debug = True
    app.run()
