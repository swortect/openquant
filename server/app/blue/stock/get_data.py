from flask import render_template,Blueprint,current_app,request,jsonify
# from app.models import *
# from app import db
import akshare as ak
import pandas as pd
import numpy as np
from app import zinc,mongo,cache,scheduler
import talib 
from datetime import datetime, timedelta,time,date
import time
import os
import json
from bson import ObjectId
import matplotlib.pyplot as plt
import random
from app.dict import stockFieldDict 
import math
from threading import Thread
get_data = Blueprint('stock/get_data', __name__)



@cache.cached(key_prefix="stock_list_base")
def getStockListBase():
    rss=[]
    aaa=[{'range':{'_id':{'gt':0}}},{'match_all':{}}]
    where={'bool':{'must':aaa}}
    pager=500
    res=zinc.index('stock').field(['stock_code','stock_name']).where(where).limit(0,pager).query()
    result = list(map(lambda x: dict({'stock_code':x['stock_code'],'stock_name':x['stock_name']}), res['res'])) 
    rss = [*rss, *result]
    for p in range(1,math.ceil(res['total']/pager)):
        res=zinc.index('stock').where(where).limit(p,pager).query()

        result = list(map(lambda x: dict({'stock_code':x['stock_code'],'stock_name':x['stock_name']}), res['res'])) 

        rss = [*rss, *result]
    return rss

@get_data.route("/test", methods=["GET"])
def test():


    pipeline = [
        # 根据 date 字段进行分组
        {
            '$group': {
                '_id': '$date',
                'date': {
                    '$first': '$date'
                }
            }
        },
        # 只返回 date 字段
        {
            '$project': {
                '_id': 0,
                'date': 1
            }
        },
        {
            '$sort': { 'date': 1 }
        }
    ]
    result = mongo.db.stock_daily_test.aggregate(pipeline)
    for date in result:
        dt = datetime.fromtimestamp(int(date['date']))
        # datetime 转字符串
        startTimeStr = dt.strftime('%Y-%m-%d %H:%M:%S')
        print(startTimeStr)
    return {
        "info": 'ok',
        "data": [],
        "status": 1,
    }
# 获取前一日股票信息
@get_data.route("/get_stock_daily")
def get_stock_daily():
    startTime=0
    startTimeStr = request.args.get('start_time', '')
    p = int(request.args.get('p', 1))
    title = request.args.get('q', '')
    pager = int(request.args.get('page_size', 50))
    if startTimeStr!='':
        startTime=math.ceil(time.mktime(time.strptime(startTimeStr, "%Y-%m-%d")))
    else:
        lastDate=mongo.db.stock_daily_test.find_one(
            sort=[('date', -1)],  # 按照 date 字段倒序排序
            projection={'_id': 0, 'date': 1}  # 只返回 date 字段
        )
        startTime=int(lastDate['date']) if lastDate else 1680796800
        dt = datetime.fromtimestamp(startTime)
        # datetime 转字符串
        startTimeStr = dt.strftime('%Y-%m-%d')
        startTime=math.ceil(time.mktime(time.strptime(startTimeStr, "%Y-%m-%d")))
    where={"date": { '$gte' : startTime,'$lte' : startTime+86399 },'mfi' : { '$gt' : 0 }}
    if title!='':
        where['$or'] = [
            { 'stock_name': { '$regex': title, '$options': 'i' } },
            { 'stock_code': { '$regex': title, '$options': 'i' } }
        ]
    print(where)
    res=mongo.db.stock_daily_test.find(where).sort('mfi', 1).skip((p-1)*pager).limit(pager)
    print(res)
    # lists = list(map(lambda x: x, res)) 
    lists = [{k: v for k, v in d.items() if k != '_id'} for d in res]

    lists = list(map(lambda s: {**s, 'stock_url': 'http://quote.eastmoney.com/unify/r/0.'+s['stock_code']}, lists))
    # print(lists)
    total=mongo.db.stock_daily_test.count_documents(where)
    return {
        "msg": 'ok',
        "data": {"list":lists,'total':total,"info":{},"start_time":startTimeStr},
        "code": 200,
    }
# 获取前一日股票信息
@get_data.route("/set_stock_daily")
def set_stock_daily():
    print(datetime.now())
    startTimeStr = request.args.get('start_time', '')
    kwargs = {'start_time': startTimeStr} 
    # timestamp = str(int(time.time()))  # 获取当前时间戳并转换为整数
    # random_num = str(random.randint(1000, 9999))  # 生成4位随机数
    # jonId = timestamp + random_num  # 将时间戳和随机数拼接起来
    # scheduler.add_job(id=jonId,func='app.blue.stock.get_data:do_set_stock_daily', trigger='date', kwargs=kwargs, run_date=datetime.now()+timedelta(seconds=2))
    # scheduler.start()
    job_thread = Thread(target=do_set_stock_daily, kwargs=kwargs)
    job_thread.start()
    return {
        "msg": '同步任务已经提交',
        "data": '',
        "code": 200,
    }
# 获取前一日股票信息
@get_data.route("/do_set_stock_daily")
def do_set_stock_daily(**kwargs):
    startTimeStr = kwargs.get('start_time', '')
    all_stocks= mongo.db.stock_info.find()
    sumcount=mongo.db.stock_info.count_documents({})
    for i in all_stocks:
        dailyData=getRsi(i['stock_code'],i['stock_name'],startTimeStr) 
        # print(dailyData) 
        if 'date' in dailyData:
            res=mongo.db.stock_daily_test.find_one({'date': dailyData['date'],'stock_code': dailyData['stock_code']})
            if res == None:
                mongo.db.stock_daily_test.insert_one(dailyData) 
            sumcount-=1
            print(sumcount) 
    return {
        "msg": 'ok',
        "data": '',
        "code": 200,
    }
# 获取单个股票详情
@get_data.route("/get_stock_detail", methods=["GET"])
def get_stock_detail():
    StockCode = request.args.get('stock_code', '')
    if StockCode!='':
        if StockCode=='au':
            data = ak.spot_hist_sge(symbol='Au(T+D)')
            data.drop([len(data)-1],inplace=True)
        else:
            end_time = time.strftime('%Y%m%d',time.localtime(time.time()))
            start_year = int(time.strftime('%Y',time.localtime(time.time()))) - 2
            month_day = time.strftime('%m%d',time.localtime(time.time()))
            start_time = '{}{}'.format(start_year,month_day)
            data = ak.stock_zh_a_hist(symbol=StockCode, period="daily", start_date=start_time, end_date=end_time, adjust="")
            stockColumn = [] 
            for field in data.columns:
                stockColumn.append(stockFieldDict[field]['field_name'])
            data.columns = stockColumn
            data['mfi'] = talib.MFI(data['highest'],data['lowest'],data['close'],data['volume'],14) 
            data['mfi'] =data['mfi'].fillna(0) 
        data['rsi6'] = talib.RSI(data['close'].values, timeperiod = 6)   
        data['rsi6'] =data['rsi6'].fillna(0) 
        data['rsi12'] = talib.RSI(data['close'].values, timeperiod = 12)  
        data['rsi12'] =data['rsi12'].fillna(0)  
        data['rsi24'] = talib.RSI(data['close'].values, timeperiod = 24) 
        data['rsi24'] =data['rsi24'].fillna(0)    
        data['upper'],data['middle'],data['lower'] = talib.BBANDS(data['close'].values,20,matype = talib.MA_Type.EMA)
        data['upper'] =data['upper'].fillna(0) 
        data['middle'] =data['middle'].fillna(0) 
        data['lower'] =data['lower'].fillna(0) 
        data.dropna(axis=0,how='any') 
        data=data.tail(300)
    lists=data.to_dict('records')
    info=mongo.db.stock_info.find_one({'stock_code': StockCode})
    info['_id'] = str(info['_id'])
    return {
        "msg": 'ok',
        "data": {"list":lists,"info":info},
        "code": 200,
    }
def out_date(x):
    publishtime = x
    array = time.strptime(publishtime, '%a, %d %b %Y %H:%M:%S GMT+0800 (CST)')
    publishTime = time.strftime("%Y-%m-%d", array)
    return publishTime
def dealNan(num):
    if str(num)=='nan': 
        return 0.00
    return num
def getRsi(StockCode,StockName,startTimeStr=''):
    # print(StockCode)
    print(startTimeStr)
    if startTimeStr=='':
        end_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        # start_year = int(time.strftime('%Y',time.localtime(time.time()))) - 2
        # month_day = time.strftime('%m%d',time.localtime(time.time()))
        # start_time = '{}{}'.format(start_year,month_day)
    else:
        dt_object = datetime.strptime(startTimeStr, '%Y-%m-%d')
        end_time = dt_object.strftime('%Y%m%d')
    dt = date(int(end_time[:4]), int(end_time[4:6]), int(end_time[6:]))

    # 计算两年前的日期
    two_years_ago = dt - timedelta(days=365 * 2)

    # 格式化为指定的日期字符串格式
    start_time = two_years_ago.strftime('%Y%m%d')

    # print(start_time)

    # print(end_time)
    # exit()
    # StockCode='600926'
    data = ak.stock_zh_a_hist(symbol=StockCode, period="daily", start_date=start_time, end_date=end_time, adjust="")
    
    stockColumn = [] 
    for field in data.columns:
        stockColumn.append(stockFieldDict[field]['field_name'])
    data.columns = stockColumn
    if 'close' not in data:
        return 0.00,0.00,0.00,0.00
    data=data.tail(300)
    data['rsi6'] = talib.RSI(data['close'].values, timeperiod = 6)   
    data['rsi12'] = talib.RSI(data['close'].values, timeperiod = 12)   
    data['rsi24'] = talib.RSI(data['close'].values, timeperiod = 24)  
    data['mfi'] = talib.MFI(data['highest'],data['lowest'],data['close'],data['volume'],14)  
    data['upper'],data['middle'],data['lower'] = talib.BBANDS(data['close'].values,20,matype = talib.MA_Type.EMA)
    data=data.tail(1)
    lists=data.to_dict('records')
    Cdate=lists[0]['date']
    lists[0]['date']=math.ceil(time.mktime(time.strptime(lists[0]['date'], "%Y-%m-%d")))

    lists[0]['rsi6']=round(dealNan(lists[0]['rsi6']),2)
    lists[0]['rsi12']=round(dealNan(lists[0]['rsi12']),2)
    lists[0]['rsi24']=round(dealNan(lists[0]['rsi24']),2)
    lists[0]['mfi']=round(dealNan(lists[0]['mfi']),2)
    lists[0]['upper']=round(dealNan(lists[0]['upper']),2)
    lists[0]['middle']=round(dealNan(lists[0]['middle']),2)
    lists[0]['lower']=round(dealNan(lists[0]['lower']),2)
    lists[0]['stock_name']=StockName
    lists[0]['stock_code']=StockCode
    lists[0]['tail_buy']=0
    

    stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol=StockCode, start_date=Cdate+" 09:30:00", end_date=Cdate+" 15:32:00", period='1', adjust='')
    stockColumn = [] 
    for field in stock_zh_a_hist_min_em_df.columns:
        stockColumn.append(stockFieldDict[field]['field_name'])
    stock_zh_a_hist_min_em_df.columns = stockColumn
    if len(stock_zh_a_hist_min_em_df)>0:
        df1 = stock_zh_a_hist_min_em_df[0:210][['close']]['close'].max()
        df2 = stock_zh_a_hist_min_em_df[211:len(stock_zh_a_hist_min_em_df)][['close']]['close'].mean()
        if df2 > df1:
            lists[0]['tail_buy']=1
    return lists[0]