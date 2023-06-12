from flask import Flask,request,jsonify
import akshare as ak
import pandas as pd
import numpy as np
import talib 
from datetime import datetime, timedelta,time
import time
import os
import matplotlib.pyplot as plt

app = Flask(__name__) 

def out_date(x):
    publishtime = x
    array = time.strptime(publishtime, '%a, %d %b %Y %H:%M:%S GMT+0800 (CST)')
    publishTime = time.strftime("%Y-%m-%d", array)
    return publishTime
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app.after_request(after_request)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
@app.route("/get_stock_daily")
def get_stock_daily():
    allStocksCacheKey = 'cache_all_stocks.pkl'
    if(os.path.exists(allStocksCacheKey)==False):
        all_stocks=ak.stock_zh_a_spot_em()
        all_stocks.to_pickle(allStocksCacheKey)
    else:
        all_stocks = pd.read_pickle(allStocksCacheKey)
    # all_stocks=all_stocks.head(100)
    sumcount=all_stocks.shape[0]
    for index, row in all_stocks.iterrows():
        # print(row['代码'])
        rsi=getRsi(row['代码'],row['名称'])
        all_stocks.at[index,'rsi6']=rsi[0]
        all_stocks.at[index,'rsi12']=rsi[1]
        all_stocks.at[index,'rsi24']=rsi[2]
        all_stocks.at[index,'mfi']=rsi[3]
        sumcount-=1
        print(sumcount)
    data = all_stocks[all_stocks["名称"].str.contains('退')==False] 
    sort_df = data.sort_values(by="mfi") 
    end_times = time.strftime('%Y%m%d',time.localtime(time.time())) 
    sort_df.to_excel("mfi"+end_times+".xlsx")  
    print(sort_df)
@app.route("/get_stock_detail")
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
            data.columns = ['date','open','close','highest','lowest','volume','turnover','amplitude','updownrange','updownnum','turnoverrate']
            data['mfi'] = talib.MFI(data['highest'],data['lowest'],data['close'],data['volume'],14)  
        data['rsi6'] = talib.RSI(data['close'].values, timeperiod = 6)   
        data['rsi12'] = talib.RSI(data['close'].values, timeperiod = 12)   
        data['rsi24'] = talib.RSI(data['close'].values, timeperiod = 24)      
        data['upper'],data['middle'],data['lower'] = talib.BBANDS(data['close'].values,20,matype = talib.MA_Type.EMA)
        data.dropna(axis=0,how='any') 
        data=data.tail(300)
        print(data)
    lists=data.to_dict('records')
    return {
        "info": '',
        "data": {"list":lists,"info":{}},
        "status": 1,
    }