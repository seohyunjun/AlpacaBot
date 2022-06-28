
import pymysql
import pandas as pd

def lee_invest_result(dict_list):
    #dict_list = seo_list
    stock_list = pd.DataFrame(dict_list,index=[0])
    Ticker = list(stock_list.columns)
    CNT = list(stock_list.values[0])

    db, cursor = DBconnect()
    cursor.execute("SELECT * FROM INVEST")
    INVEST = pd.DataFrame(cursor.fetchall())
    INVEST.columns = ['NAME','TICKER','PRICE','CNT','AMOUNT','CASH']
    LEE = INVEST[INVEST['NAME']=='LEE']
    total = []
    lee_profit = 0
    lee_msg = ''
    for T,price,cnt in zip(LEE['TICKER'],LEE['PRICE'],LEE['CNT']):

        start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
        now = datetime.today().strftime('%Y-%m-%d')
        Time = int(datetime.today().strftime('%H'))
        Stock = StockData(T,start,now,time='min')
        data = Stock.load_data_alpaca()
        data.sort_values('DATE',inplace=True)
        value = data['CLOSE'][-1]
        
        lee_msg=lee_msg+f"""{T.upper()}({cnt}): {value}-{price} {(value-price)/price*100:.2f}%
        """
        lee_profit = lee_profit + ((value-price) * cnt)
    lee_msg = lee_msg+ f'''
    profit:{lee_profit+LEE['CASH'].iloc[0]:.2f} {(lee_profit)/(100000-LEE['CASH'].iloc[0])*100:.2f}'''
    return lee_msg



def seo_invest_result(dict_list):
    #dict_list = seo_list
    stock_list = pd.DataFrame(dict_list,index=[0])

    Ticker = list(stock_list.columns)
    CNT = list(stock_list.values[0])

    db, cursor = DBconnect()
    cursor.execute("SELECT * FROM INVEST")
    
    INVEST = pd.DataFrame(cursor.fetchall())
    INVEST.columns = ['NAME','TICKER','PRICE','CNT','AMOUNT','CASH']
    SEO = INVEST[INVEST['NAME']=='SEO']
    
    total = []
    seo_profit = 0
    seo_msg = ''
    for T,price,cnt in zip(SEO['TICKER'],SEO['PRICE'],SEO['CNT']):
        
        start = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
        now = datetime.today().strftime('%Y-%m-%d')
        Time = int(datetime.today().strftime('%H'))
        Stock = StockData(T,start,now,time='min')
        data = Stock.load_data_alpaca()
        value = data['CLOSE'][-1]
        seo_profit += (value - price) * cnt
        seo_msg=seo_msg+f"""{T.upper()}({cnt}): {value}-{price} {(value-price)/price*100:.2f}%
        """
        seo_profit = seo_profit + ((value-price) * cnt)
    seo_msg = seo_msg+ f'''
    profit:{seo_profit+SEO['CASH'].iloc[0]:.2f} {(seo_profit)/(100000-SEO['CASH'].iloc[0])*100:.2f}'''

    return seo_msg