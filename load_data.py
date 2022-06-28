from datetime import datetime, timedelta
from alpaca_trade_api.rest import REST, TimeFrame #alpaca load api
import pandas as pd
import time

import requests
import json

import pymysql
# https://apps.timwhitlock.info/emoji/tables/unicode



# Client ID:
# PKWZ3J8AEQYSBJVKK1MW

# Client Secret:
# 1r7TUmFUlnETLAdlTtzUeJcJqYXaldCWygC21GQK
##if __name__=='__main__':

#CLEARDB_DATABASE_URL: mysql://b58af86981239b:7ab127ce@us-cdbr-east-05.cleardb.net/heroku_c41a079ed6d7ed3?reconnect=true

def DBconnect():
    #데이터 입력용 conn
    db = pymysql.connect(
        host='us-cdbr-east-05.cleardb.net',
        port=3306,
        user='b58af86981239b',
        passwd='7ab127ce',
        db='heroku_c41a079ed6d7ed3',
        charset='utf8')
    cursor = db.cursor()
    return db,cursor
    
def load_stock_data(Ticker,start=(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d'),end=datetime.now().strftime('%Y-%m-%d')):

    cost_start = time.time()
    api = REST(
        'PKWZ3J8AEQYSBJVKK1MW',
        '1r7TUmFUlnETLAdlTtzUeJcJqYXaldCWygC21GQK')
    
    # if time_type=='min':
    #     time_t=TimeFrame.Minute
    # elif time_type=='day':
    #     time_t=TimeFrame.Day
        
    try:
        m_data = api.get_bars(Ticker, TimeFrame.Minute, start, end,adjustment='raw').df
    except:
        m_data = None

    try:
        d_data = api.get_bars(Ticker, TimeFrame.Day, start, end,adjustment='raw').df
        if len(d_data)==0:
            d_data = api.get_bars(Ticker, TimeFrame.Day, (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'),adjustment='raw').df
    except:
        d_data = None
    
    cost_end = time.time()
    cost = cost_end-cost_start
    return cost, m_data,d_data  

def messege(Ticker):
    Ticker = Ticker.upper()
    dollar = USDKRW()

    cost, m_data,d_data = load_stock_data(Ticker)
    now_price = m_data.iloc[-1,:]['open']
    last_price = d_data.iloc[-1,:]['close']
    st = now_price - last_price
    if st>=0: face="🐮🔺"
    else : face="🐻🔽"
       
    msg = f"""
    \x1BTicker\x1B :   {Ticker.upper()}
    \x1BSignal Price\x1B : {now_price}$ / {now_price*dollar:,}₩
    \x1BVolume Weight Avg.\x1B :    {m_data.iloc[-1,-1]}
    \x1BSignal Time :   {m_data.index[-1]}\x1B
    {face} {(now_price-last_price)/last_price*100:.2f} 
    """
    print(cost)
    return msg

def news_message(Ticker="LCID"):
    Ticker = Ticker.upper()
    headers = {
        'Apca-Api-Key-Id':'PKWZ3J8AEQYSBJVKK1MW',
        'Apca-Api-Secret-Key':'1r7TUmFUlnETLAdlTtzUeJcJqYXaldCWygC21GQK',
    }
    params = {
        'symbols':Ticker
    }
    req = requests.get(url = 'https://data.alpaca.markets/v1beta1/news',params=params,headers=headers)
    content = json.loads(req.content)
    if len(content['news'])==0:
        return "No Contents"
    news_msg  = [f"""
    headline: {con['headline']}({con['updated_at']})
    Summary: {con['summary']}
    """
    for con in content['news']]

    result = '\n'.join(news_msg)

    return result

def load_inv_list(name, season):

    db, cursor = DBconnect()
    cursor.execute(f'SELECT * FROM invlist WHERE NAME=\'{name}\' AND SEASON={season}')
    invdata = pd.DataFrame(cursor.fetchall())
    invdata.columns = ['SEASON','NAME','TICKER','PRICE','CNT','AMOUNT','CASH']
    
    total = []
    profit = 0
    msg = ''
    start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
    now = datetime.today().strftime('%Y-%m-%d')
        
    for T,price,cnt in zip(invdata['TICKER'],invdata['PRICE'],invdata['CNT']):

        cost, d_data, m_data = load_stock_data(T,start=start,end=now)
        d_data.sort_index(inplace=True)
        value = d_data['close'][-1]
        
        msg=msg+f"""{T.upper()}({cnt}): {value}-{price} {(value-price)/price*100:.2f}%
        """
        profit = profit + ((value-price) * cnt)
    msg = msg+ f'''
    profit:{profit+invdata['CASH'].iloc[0]:.2f} {(profit)/(100000-invdata['CASH'].iloc[0])*100:.2f}'''
    return msg
# def plt_save(data):

#     sns.lineplot(x = data.index, y = data.open)
#     plt.save()

# def load_stock_ticker(TTicker):

        
#     Ticker = Ticker
#     self.Start = Start
#     self.End = End
#     self.api = REST(
#         'PKWZ3J8AEQYSBJVKK1MW',
#         '1r7TUmFUlnETLAdlTtzUeJcJqYXaldCWygC21GQK')
#     if time=='min':
#         self.time=TimeFrame.Minute
#     elif time=='Day':
#         self.time=TimeFrame.Day
#     def load_info_data(self):
#         self.df_nasdaq = fdr.StockListing('NASDAQ')
#         return self.df_nasdaq
        
#     def info(self):
#         self.info = self.df_nasdaq[self.df_nasdaq['Symbol']==self.Ticker]   
#         return self.info
        
#     def load_data_alpaca(self):
#         self.data = self.api.get_bars(self.Ticker, self.time,self.Start,self.End,adjustment='raw').df
#         self.data.columns = [col.upper() for col in self.data.columns]
    
    
#     start = (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')
#     now = datetime.today().strftime('%Y-%m-%d')
#     Time = int(datetime.today().strftime('%H'))
#     Stock = StockData(T,start,now,time='min')
#     data = Stock.load_data_alpaca()
    
#     value = data['CLOSE'][-1]
#     D_Stock = StockData(T,start,now,time='Day')
#     D_data = D_Stock.load_data_alpaca()
#     last = D_data['CLOSE'][-2]
#     st = (value-last)/last*100
#     if len(data)==0:
#         return "None Data"
#     if st>=0: face="🐮🔺"
#     else : face="🐻🔽"

#     if (Time >= 0) & (Time <= 17):
#         end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
#         target = data[(data['DATE']>f"{end} 08:00:00")]
#     else:
#         target = data[(data['DATE']>f"{now} 08:00:00")]
    
#     Count = target['VOLUME'].sum()
#     usd = USDKRW()
    
#     KST = pytz.timezone("Asia/Seoul")
#     UTC = pytz.timezone("UTC")
#     Signal = data.iloc[-1]['DATE'].replace(tzinfo=UTC)
#     Signal = Signal.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")
    
#     if Vol==0:       
#         msg = f"""
#     \x1BTicker\x1B :   {T.upper()}
#     \x1BSignal Price\x1B : {data.iloc[-1]['OPEN']}$ / {int(data.iloc[-1]['OPEN']*usd):,}₩
#     \x1BVolume\x1B :    {Count}
#     \x1BVolume Weight Avg.\x1B :    {data.iloc[-1]['VWAP']}
#     \x1BSignal Time :   {Signal}\x1B
#     {face} {(value-last)/last*100:.2f} 
#     """
#         return msg
#     Volp = Count / Vol[0] * 100 
#     msg = f"""
# \x1BTicker\x1B :   {T.upper()}
# \x1BSignal Price\x1B : {data.iloc[-1]['OPEN']}$ / {int(data.iloc[-1]['OPEN']*usd):,}₩
# \x1BVolume\x1B :    {Count}
# \x1BVolp\x1B :  {Volp:.2f}%
# \x1BVolume Weight Avg.\x1B :    {data.iloc[-1]['VWAP']}
# \x1BSignal Time :   {Signal}\x1B
# {face} {(value-last)/last*100:.2f} 
# """
#     return msg


# def load_stock_base(T):
    
#     start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
#     now = datetime.today().strftime('%Y-%m-%d')
#     Time = int(datetime.today().strftime('%H'))
#     Stock = StockData(T,start,now,time='min')
#     data = Stock.load_data_alpaca()
    
#     value = data['CLOSE'][-1]
#     D_Stock = StockData(T,start,now,time='Day')
#     D_data = D_Stock.load_data_alpaca()
#     last = D_data['CLOSE'][-2]
#     st = (value-last)/last*100
#     if len(data)==0:
#         return "None Data"
#     if st>=0: face="🐮🔺"
#     else : face="🐻🔽"

#     if (Time >= 0) & (Time <= 17):
#         end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
#         target = data[(data['DATE']>f"{end} 08:00:00")]
#     else:
#         target = data[(data['DATE']>f"{now} 08:00:00")]
    
#     Count = target['VOLUME'].sum()
#     usd = USDKRW()
#     KST = pytz.timezone("Asia/Seoul")
#     UTC = pytz.timezone("UTC")
#     Signal = data.iloc[-1]['DATE'].replace(tzinfo=UTC)
#     Signal = Signal.astimezone(KST).strftime("%Y-%m-%d %H:%M:%S")
#     db, cursor = DBconnect()
#     Vol = cursor.execute(f"SELECT SHAERES FROM STOCK_INFO WHERE SYMBOL='{T.upper()}'")
#     Vol = [i[0] for i in cursor.fetchall()]
#     if None in Vol:       
#         msg = f"""
#     \x1BTicker\x1B :   {T.upper()}
#     \x1BSignal Price\x1B : {data.iloc[-1]['OPEN']}$ / {int(data.iloc[-1]['OPEN']*usd):,}₩
#     \x1BVolume\x1B :    {Count}
#     \x1BVolume Weight Avg.\x1B :    {data.iloc[-1]['VWAP']}
#     \x1BSignal Time :   {Signal}\x1B
#     {face} {(value-last)/last*100:.2f} 
#     """
#         return msg
#     Volp = Count / Vol[0] * 100 
#     msg = f"""
# \x1BTicker\x1B :   {T.upper()}
# \x1BSignal Price\x1B : {data.iloc[-1]['OPEN']}$ / {int(data.iloc[-1]['OPEN']*usd):,}₩
# \x1BVolume\x1B :    {Count}
# \x1BVolp\x1B :  {Volp:.2f}%
# \x1BVolume Weight Avg.\x1B :    {data.iloc[-1]['VWAP']}
# \x1BSignal Time :   {Signal}\x1B
# {face} {(value-last)/last*100:.2f} 
# """
#     return msg


def USDKRW():
    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW'
    exchange=pd.read_html(url,encoding='cp949')
    one = exchange[2].loc[0].values[1]
    return one


# def lee_invest_result(dict_list):
#     #dict_list = seo_list
#     stock_list = pd.DataFrame(dict_list,index=[0])
#     Ticker = list(stock_list.columns)
#     CNT = list(stock_list.values[0])

#     db, cursor = DBconnect()
#     cursor.execute("SELECT * FROM INVEST")
#     INVEST = pd.DataFrame(cursor.fetchall())
#     INVEST.columns = ['NAME','TICKER','PRICE','CNT','AMOUNT','CASH']
#     LEE = INVEST[INVEST['NAME']=='LEE']
#     total = []
#     lee_profit = 0
#     lee_msg = ''
#     for T,price,cnt in zip(LEE['TICKER'],LEE['PRICE'],LEE['CNT']):

#         start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
#         now = datetime.today().strftime('%Y-%m-%d')
#         Time = int(datetime.today().strftime('%H'))
#         Stock = StockData(T,start,now,time='min')
#         data = Stock.load_data_alpaca()
#         data.sort_values('DATE',inplace=True)
#         value = data['CLOSE'][-1]
        
#         lee_msg=lee_msg+f"""{T.upper()}({cnt}): {value}-{price} {(value-price)/price*100:.2f}%
#         """
#         lee_profit = lee_profit + ((value-price) * cnt)
#     lee_msg = lee_msg+ f'''
#     profit:{lee_profit+LEE['CASH'].iloc[0]:.2f} {(lee_profit)/(100000-LEE['CASH'].iloc[0])*100:.2f}'''
#     return lee_msg

# def load_lee_list():
#     lee_list = {"GRAB":2700,
#             "OPEN":1380,
#             "TSLA":10,
#             "aapl":59,
#             "GOOGL":4,
#             "MSFT":30,
#             'JPM':80,
#             "pltr":700,
#             "SNOW":50,
#             "DIS":35,
#             "NKE":35 }
#     return lee_list

# def load_seo_list():
#     seo_list = {"GRAB":2700,
#             "OPEN":1380,
#             "TSLA":10,
#             "aapl":59,
#             "GOOGL":4,
#             "MSFT":30,
#             'JPM':80,
#             "pltr":700,
#             "SNOW":50,
#             "DIS":35,
#             "NKE":35 }
#     return seo_list


# def seo_invest_result(dict_list):
#     #dict_list = seo_list
#     stock_list = pd.DataFrame(dict_list,index=[0])
#     Ticker = list(stock_list.columns)
#     CNT = list(stock_list.values[0])

#     db, cursor = DBconnect()
#     cursor.execute("SELECT * FROM INVEST")
#     INVEST = pd.DataFrame(cursor.fetchall())
#     INVEST.columns = ['NAME','TICKER','PRICE','CNT','AMOUNT','CASH']
#     SEO = INVEST[INVEST['NAME']=='SEO']
    
#     total = []
#     seo_profit = 0
#     seo_msg = ''
#     for T,price,cnt in zip(SEO['TICKER'],SEO['PRICE'],SEO['CNT']):
        
#         start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
#         now = datetime.today().strftime('%Y-%m-%d')
#         Time = int(datetime.today().strftime('%H'))
#         Stock = StockData(T,start,now,time='min')
#         data = Stock.load_data_alpaca()
#         value = data['CLOSE'][-1]
#         seo_profit += (value - price) * cnt
#         seo_msg=seo_msg+f"""{T.upper()}({cnt}): {value}-{price} {(value-price)/price*100:.2f}%
#         """
#         seo_profit = seo_profit + ((value-price) * cnt)
#     seo_msg = seo_msg+ f'''
#     profit:{seo_profit+SEO['CASH'].iloc[0]:.2f} {(seo_profit)/(100000-SEO['CASH'].iloc[0])*100:.2f}'''

#     return seo_msg


