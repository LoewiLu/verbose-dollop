import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import urllib.request
import json


def import_data(ticker, timeseries):
    if timeseries == 'intraday':
        #intraday 指的是一天内的交易数据 #add your own API from https://www.alphavantage.co/support/#api-key
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+ticker +'&interval=1min&apikey='+ 'api' +'&outputsize=full&datatype=json'
        name = 'Time Series (1min)'
    if timeseries == 'daily':
        #daily指的是每一天的交易数据 #add your own API
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker +'&apikey='+ 'api' +'&outputsize=compact&datatype=json'
        name = 'Time Series (Daily)'
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    js = mybytes.decode("utf8")
#     print(js)
    fp.close()
    parsed_data = json.loads(js) #读取json数据并且将json转化成字典
    ps = parsed_data[name]
    df = pd.DataFrame.from_dict(ps, orient='index')
    df.columns = ['Open','High','Low','Close','Volume'] #将每一列的名字领名
    return df

#读取 AAPL 的交易数据
apple = import_data('AAPL', 'daily') #'GOOGL'/'GOOG'; 'MSFT'
cols = apple.columns
apple[cols] = apple[cols].apply(pd.to_numeric, errors='coerce') #将每一列转化成数字变量
apple.index = pd.to_datetime(apple.index, format='%Y-%m-%d') #将索引转化成时间变量

plt.figure(figsize=(10,5))  # 改变图片大小
apple["Close"].plot(grid = True)
plt.title('Close Price of AAPL')
plt.show()

#改写成公式
def data_clean(df):
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    return df
#获取多个公司的数据
company_list = ['GOOGL','MSFT','FB']
stock_list ={}
try:
    for company in company_list:
        print("Starting with " + company)
        df = import_data(company, 'daily')
        stock_list[company] = data_clean(df)
        print("Ended Writing Data of " + company)
except Exception as e:
    print(e)

#蜡烛图
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, date2num
from matplotlib.finance import candlestick_ohlc, candlestick2_ochl
import datetime
from datetime import date
import pylab

#怎么使用candlestick_ohlc(candlestick2_ochl)
#matplotlib.finance.candlestick_ohlc(ax, quotes, width=0.2, colorup='k', colordown='r', alpha=1.0)
#https://matplotlib.org/api/finance_api.html

mondays = WeekdayLocator(MONDAY)        #用于横坐标设定，每个显示的横坐标都是周一
alldays = DayLocator()              #横坐标的最小单位为一天

%pylab inline
pylab.rcParams['figure.figsize'] = (15, 9)      #设置图片的大小
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
weekFormatter = DateFormatter('%b %d, %Y')  #设置坐标显示的日期格式Jun 5, 2018
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
ax.grid(True)
candlestick_ohlc(ax, list(zip(list(date2num(apple.index.tolist())), apple["Open"].tolist(), apple["High"].tolist(),
                 apple["Low"].tolist(), apple["Close"].tolist())),
                 colorup = "red", colordown = "green", width = 1 * .4)
# candlestick2_ochl(ax, apple["Open"].tolist(), apple["Close"].tolist(), apple["High"].tolist(),
#                  apple["Low"].tolist(),
#                  colorup = "red", colordown = "green", width = 1 * .4, alpha=0.75)
ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.title('AAPL')
plt.show()


#对图上某一个位置的数据进行标注¶
dt = date2num(date(2018, 4, 9))
ax.annotate(str(apple.loc['2018-04-09','High']), xy=(dt-2, 175))
ax.annotate(str(apple.loc['2018-04-09','Low']), xy=(dt-2, 168))
#关于datetime的很多用法
#https://docs.python.org/3/library/datetime.html
#groupby的用法
#https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html
#当需要显示的数据周期是周，月，年
def pandas_candlestick_ohlc(dat, ticker, lag = "day", label_date = None, x1=0, x2=0):
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()

    transdat = dat.loc[:,["Open", "High", "Low", "Close"]]
    if (type(lag) == str):
        if lag == "day":
            plotdat = transdat
            w = 1
        elif lag in ["week", "month", "year"]:
            if lag == "week":
                transdat["week"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[1]) #定义每一周
                w = 7
            elif lag == "month":
                transdat["month"] = pd.to_datetime(transdat.index).map(lambda x: x.month) #定义一个月
                w = 30
            elif lag == "year":
                w = 365
            transdat["year"] = pd.to_datetime(transdat.index).map(lambda x: x.isocalendar()[0]) #定义一年
            grouped = transdat.groupby(list(set(["year",lag])))
            plotdat = pd.DataFrame({"Open": [], "High": [], "Low": [], "Close": []})
            for name, group in grouped:
                plotdat = plotdat.append(pd.DataFrame({"Open": group.iloc[0,0],
                                            "High": max(group.High),
                                            "Low": min(group.Low),
                                            "Close": group.iloc[-1,3]},
                                           index = [group.index[0]]))
    else:
        raise ValueError('Valid inputs to argument "lag" include the strings "day", "week", "month", "year"')


    pylab inline
    pylab.rcParams['figure.figsize'] = (15, 9)
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.grid(True)

    candlestick_ohlc(ax, list(zip(list(date2num(plotdat.index.tolist())), plotdat["Open"].tolist(), plotdat["High"].tolist(),
                      plotdat["Low"].tolist(), plotdat["Close"].tolist())),
                      colorup = "red", colordown = "green", width = w* .4)

    if label_date != None:
        dt = date2num(datetime.datetime.strptime(label_date,'%Y-%m-%d').date())
        ax.annotate(str(apple.loc[label_date,'High']), xy=(dt-2, x1))
        ax.annotate(str(apple.loc[label_date,'Low']), xy=(dt-2, x2))

    ax.xaxis_date()
    ax.autoscale_view()
    plt.title(ticker)
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

pandas_candlestick_ohlc(apple.loc['2018-02-14':'2018-05-14',:], ticker = 'AAPL', lag = 'day',label_date = '2018-04-09',x1 = 175, x2 = 168)
