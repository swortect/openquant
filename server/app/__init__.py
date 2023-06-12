from flask import Flask,Blueprint
# from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from config import Config
from app.utils.zinc import Zinc
from flask_pymongo import PyMongo
from flask_caching import Cache
import time
# 实例化
app = Flask(__name__)
app.host = '0.0.0.0'
app.port = 5000
app.debug = True

app.config.from_object(Config)
# db = SQLAlchemy()
# # 绑定db
# db.init_app(app)
zinc=Zinc()
zinc.setApp(app)

mongo = PyMongo()
mongo.init_app(app)
cache = Cache(app)

scheduler = APScheduler()
scheduler.init_app(app)
# 表示一天后开始执行，然后每天执行一次
# scheduler.add_job(id='stockGetDaily', func='cron.stock:getDaily',
#                   trigger='interval', day=1, args=[app, ])
scheduler.start()

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization,Content-Type,token'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/user/permission")
def user_permission():
    return {
    'code': 200,
    'msg': "操作成功",
    'data': ['sys:user:add','sys:user:edit','sys:user:delete','sys:user:import','sys:user:export'],
    'success': True
  }
@app.route("/user/menu")
def user_menu():
    menus=[{
    'id': "/workspace",
    'icon': "layui-icon-home",
    'title': "工作空间",
    'children': [
      {
        'id': "/stock/index",
        'icon': "layui-icon-home",
        'title': "股票列表"
      },
      {
        'id': "/chat/index",
        'icon': "layui-icon-home",
        'title': "chatgpt"
      },
      {
        'id': "/table/base",
        'icon': "layui-icon-home",
        'title': "查询列表"
      },
      {
        'id': "/table/card",
        'icon': "layui-icon-home",
        'title': "卡片列表"
      }
    ]

    }]
    return {
    'code': 200,
    'msg': "操作成功",
    'data': menus,
    'success': True
  }

# 注册蓝图
# from app.blue.home import home as home_blueprint
from app.blue.stock import stock as stock_blueprint


# app.register_blueprint(home_blueprint)
app.register_blueprint(stock_blueprint, url_prefix='/stock')



