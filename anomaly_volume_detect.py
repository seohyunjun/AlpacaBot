import load_data
import pandas as pd
import pytz
from datetime import timedelta, timezone, tzinfo, datetime

from statsmodels.tsa.seasonal import seasonal_decompose

if __name__=='__main__':

    start = (datetime.now()-timedelta(days=365*2)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    T = 'TSLA'
    Stock = load_data.StockData(T,Start=start,End=end)
    M_data = Stock.load_data_alpaca()
    Stock = load_data.StockData(T,Start=start,End=end,time='Day')
    D_data = Stock.load_data_alpaca()

    # count share
    db, cursor = load_data.DBconnect()
    cursor.execute(f"SELECT SHAERES FROM STOCK_INFO WHERE SYMBOL = '{T}'")
    total_share = pd.DataFrame(cursor.fetchall(),columns=['SHAERES'])
    db.close()

    # KST = pytz.timezone("Asia/Seoul")
    # UTC = pytz.timezone("UTC")
    # data['DATE'] = [date.replace(tzinfo=UTC).astimezone(KST) for date in data['DATE']]
    M_data.sort_index(inplace=True)
    D_data.sort_index(inplace=True)
    M_data['Time'] = [datetime.strptime(time,'%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S') for time in M_data['DATE']]
    M_data['Day'] = [datetime.strptime(time,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') for time in M_data['DATE']]

    t_data = M_data[(M_data['Time']>'17:00:00') & (M_data['Time']<'22:00:00')]

    

    base = []
    for date in t_data['Day'].drop_duplicates():
        temp = {"Day":date, "base":t_data[t_data['Day']==date].iloc[0]['OPEN']}
        base.append(temp)
    
    base = pd.DataFrame(base)
    t_data = pd.merge(t_data, base,on='Day',how='inner')

    pre_data = pd.DataFrame()
    pre_data['open_rate'] = t_data['OPEN'] / t_data['base']
    pre_data['close_rate'] = t_data['CLOSE'] / t_data['base']
    pre_data['low_rate'] = t_data['LOW'] / t_data['base']
    pre_data['vwap_rate'] = t_data['VWAP'] / t_data['base']
    pre_data['volume'] = t_data['VOLUME'] / total_share['SHAERES'][0] * 10000
    pre_data['trade_count'] = t_data['TRADE_COUNT'] 
    pre_data['num'] = sum([list(range(len(t_data[t_data['Day']==day]))) for day in t_data['Day'].drop_duplicates()],[])
    pre_data['anomaly'] = [ 1 if an>=1.03 else 0 for an in pre_data['open_rate']]
    
    date_num = []
    num=0
    for day in t_data['Day'].drop_duplicates():
        date_num.append([num]*len(t_data[t_data['Day']==day]))
        num+=1
    
    pre_data['day_num'] = sum(date_num,[])
    
    #input : Time, price_rate, volume_rate, trade_count, vmap_rate