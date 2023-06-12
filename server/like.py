import pandas_datareader as pdr
import ta
import numpy as np
import akshare as ak
import time
 # 获取股票价格数据
start_date = '2021-01-01'
end_date = '2021-12-31'
# df = pdr.get_data_yahoo(symbol, start_date, end_date)
StockCode="600415"
end_time = time.strftime('%Y%m%d',time.localtime(time.time()))

start_year = int(time.strftime('%Y',time.localtime(time.time()))) - 2
month_day = time.strftime('%m%d',time.localtime(time.time()))
start_time = '{}{}'.format(start_year,month_day)

take_end_time='20230601' 
df = ak.stock_zh_a_hist(symbol=StockCode, period="daily", start_date=start_time, end_date=take_end_time, adjust="")
df.columns = ['date','open','close','highest','lowest','volume','turnover','amplitude','updownrange','updownnum','turnoverrate']

# print(df['close'])
 # 计算MACD指标
macd_indicator = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
df['macd'] = macd_indicator.macd()
df['macdsignal'] = macd_indicator.macd_signal()
df['macdhist'] = macd_indicator.macd_diff()
df=df.tail(365)
print(df)
exit()
 # 提取MACD指标数据
macd_data = df[['macd', 'macdsignal', 'macdhist']].values
 # 标准化MACD指标数据
mean = np.mean(macd_data, axis=0)
std = np.std(macd_data, axis=0)
macd_data = (macd_data - mean) / std
 # 计算股票之间的相似性
distances = []

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
symbols =stock_zh_a_spot_em_df['代码'].tolist()
# symbols = ['600415', '002857', '600757', '600926', '000516']
for s in symbols:
    # 获取股票价格数据
    # df = pdr.get_data_yahoo(s, start_date, end_date)
    df = ak.stock_zh_a_hist(symbol=s, period="daily", start_date=start_time, end_date=end_time, adjust="")
    if len(df.columns) < 11:
        print("列数小于11，跳出循环")
        break
    df.columns = ['date','open','close','highest','lowest','volume','turnover','amplitude','updownrange','updownnum','turnoverrate']
    macd_indicator = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd_indicator.macd()
    df['macdsignal'] = macd_indicator.macd_signal()
    df['macdhist'] = macd_indicator.macd_diff()
    df=df.tail(365)
     # 提取MACD指标数据
    macd_data2 = df[['macd', 'macdsignal', 'macdhist']].values
     # 标准化MACD指标数据
    macd_data2 = (macd_data2 - mean) / std
     # 计算欧几里得距离
    if macd_data.shape == macd_data2.shape:
        distance = np.linalg.norm(macd_data - macd_data2)
        distances.append({'stock_code':s,'distance':distance}) 
        print(s+"down") 
    else:
        print(s+"jump") 
sorted_data = sorted(distances, key=lambda x: x['distance'])[:10]
print(sorted_data) 
#  # 输出相似性最高的股票
# most_similar_index = np.argmin(distances)
# most_similar_symbol = symbols[most_similar_index]
# print(f"The most similar stock to {StockCode} based on MACD is {most_similar_symbol}")