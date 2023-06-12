from flask import render_template,Blueprint,g,make_response,jsonify,request
from app.models import *
from app import db
import time
import subprocess

import json
special = Blueprint('special', __name__)


# 一个函数，用来做定时任务的任务。
def cronspider(a,b):
    rs = HzSpecialUrl.query.order_by(HzSpecialUrl.id.desc()).all()
    for i in rs:
        runspider(project="news",spider=i.spider_name,url_id=str(i.id))

def runspider(project="news",spider="netease",url_id="1"):

    clss = f'/home/wwwroot/python/spider/spider.sh {project} {spider} {url_id}'
    #print(clss.split(" "))
    subprocess.Popen(clss.split(" "))

@special.route("/", methods=["GET"])
@special.route("/index", methods=["GET"])
def _index():
    rs = HzSpecial.query.filter( HzSpecial.status==1).order_by(HzSpecial.id.desc()).limit(10).all()

    return render_template('/home/special/index.html',rs=rs)
@special.route("/add", methods=["GET"])
def add():
    return render_template('/home/special/add.html')
    
@special.route("/special_post", methods=["POST"])
def special_post():
    special_name = request.form['special_name']
    print(special_name)
    #special_name = 'special_name'
    if special_name =='':
        response = make_response(jsonify({'status': 0, 'info': "热点名缺失", 'data': {"refer":1}}))
        return response
    insert = HzSpecial(special_name=special_name)
    db.session.add(insert)
    db.session.commit()
    response = make_response(jsonify({'status': 1, 'info': "添加成功", 'data': {"refer":1}}))
    return response





@special.route("/spider", methods=["GET"])
def spider():
    # 创建一个CrawlerProcess对象
    # settings = get_project_settings()
    # process = CrawlerProcess(settings=settings)  # 括号中可以添加参数
    #
    # process.crawl(BookSpider, sub_id=1116367)
    # # process.crawl(BookSpider,sub_id=5243775)
    # process.start()
    # spider_name = "book"
    # spider_path=r"H: cd python\college\flasks\layui\spider\douban\ "
    # clss=spider_path+'scrapy crawl '+spider_name+" -a sub_id=1116367"
    # print(clss.split(" "))
    # subprocess.check_output(clss.split(" "))
    #subprocess.check_output(['scrapy', 'crawl', spider_name])
    url_id = int(request.args.get("id"))
    print(url_id)

    
    rs = HzSpecialUrl.query.filter(HzSpecialUrl.id==url_id).first()
    if (rs is None):
        response = make_response(jsonify({'status':0, 'info': "链接不存在", 'data': {"refer":1}}))
        return response
    #runspider(project="news",spider=rs.spider_name,url_id=str(id))
    print(rs.id)
    last_time=int(time.time())
    #HzSpecialUrl.query.filter(rs.id=id).update({'last_time':last_time})

    #rs.last_time=last_time
    #HzSpecialUrl.query.filter(HzSpecialUrl.id==url_id).update({HzSpecialUrl.last_time:last_time}, synchronize_session=False) 
    #db.session.commit() 
    HzSpecialUrl.set_last_time(url_id,last_time)

    response = make_response(jsonify({'status': 1, 'info': "启动成功", 'data': {"refer":1}}))
    return response
@special.route("/urls", methods=["GET"])
def urls():
    id = int(request.args.get("id"))
    rs = HzSpecialUrl.query.filter( HzSpecialUrl.special_id==id).order_by(HzSpecialUrl.id.desc()).limit(10).all()
    return render_template('/home/special/urls.html',rs=rs,special_id=id) 
@special.route("/add_url", methods=["GET"])
def add_url():
    special_id = request.args.get("special_id",type=int,default=0) 
    return render_template('/home/special/add_url.html',special_id=special_id)

@special.route("/post_url", methods=["POST"])
def post_url():
    special_url = request.form['special_url']
    spider_name = request.form['spider_name']
    spider_key = request.form['spider_key']
    special_id = request.form['special_id']
    print(spider_key)
    #special_name = 'special_name'
    if special_url =='':
        response = make_response(jsonify({'status': 0, 'info': "请输入新闻链接", 'data': {"refer":1}}))
        return response
    if spider_key =='':
        response = make_response(jsonify({'status': 0, 'info': "请输入新闻ID", 'data': {"refer":1}}))
        return response
    insert = HzSpecialUrl(special_url=special_url,spider_name=spider_name,spider_key=spider_key,special_id=special_id)
    db.session.add(insert)
    db.session.commit()
    response = make_response(jsonify({'status': 1, 'info': "添加成功", 'data': {"refer":1}}))
    return response




@special.route("/comment", methods=["GET"])
def comment():
    id = request.args.get("id",type=int,default=0)
    q = request.args.get("q",type=str,default="")
    p = request.args.get("p",type=int,default=1)
    pager=50
    offset=(p-1) * pager
    if q != "":
        rs = HzSpecialComment.query.filter( HzSpecialComment.special_id==id,HzSpecialComment.comment.like("%" + q + "%")).order_by(HzSpecialComment.id.desc()).limit(pager).offset(offset).all()
    else:
        rs = HzSpecialComment.query.filter( HzSpecialComment.special_id==id).order_by(HzSpecialComment.id.desc()).limit(pager).offset(offset).all()

    aa = HzSpecialComment.query.filter( HzSpecialComment.special_id==id, HzSpecialComment.score1 >= 0.5).count()  
    bb = HzSpecialComment.query.filter( HzSpecialComment.special_id==id, HzSpecialComment.score1 < 0.5).count()  
    daily_count = HzSpecialComment.daily_count(id)
    xAxis=daily_count['xAxis']
    series=daily_count['series']
    return render_template('/home/special/comment.html',rs=rs,aa=aa,bb=bb,xAxis=xAxis,series=series,q=q,id=id)


